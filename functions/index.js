const functions = require('firebase-functions');
const admin = require('firebase-admin');

admin.initializeApp();

// ── Helper: Send push notification to all subscribed tokens ──
async function sendNotificationToAll(title, body) {
  const tokensSnapshot = await admin.database().ref('fcmTokens').once('value');
  const tokensData = tokensSnapshot.val() || {};

  const tokens = Object.values(tokensData)
    .map(t => t.token)
    .filter(t => t);

  if (tokens.length === 0) {
    console.log('No FCM tokens to send to.');
    return { successCount: 0, failureCount: 0 };
  }

  const message = {
    notification: { title, body },
    tokens: tokens
  };

  const response = await admin.messaging().sendEachForMulticast(message);
  console.log(`Sent: ${response.successCount} success, ${response.failureCount} failures`);

  // Clean up invalid tokens
  const tokensToRemove = [];
  response.responses.forEach((resp, idx) => {
    if (!resp.success) {
      const code = resp.error?.code;
      if (code === 'messaging/invalid-registration-token' ||
          code === 'messaging/registration-token-not-registered') {
        tokensToRemove.push(tokens[idx]);
      }
    }
  });

  if (tokensToRemove.length > 0) {
    const allTokens = Object.entries(tokensData);
    for (const [key, data] of allTokens) {
      if (tokensToRemove.includes(data.token)) {
        await admin.database().ref('fcmTokens/' + key).remove();
      }
    }
    console.log(`Cleaned up ${tokensToRemove.length} invalid tokens`);
  }

  return response;
}

// ── Manual Push Notification (called by admin from UI) ──
exports.sendNotification = functions.https.onCall(async (data, context) => {
  // Verify the caller is authenticated
  if (!context.auth) {
    throw new functions.https.HttpsError('unauthenticated', 'Must be signed in.');
  }

  // Verify the caller is an admin
  const adminSnap = await admin.database().ref('admins/' + context.auth.uid).once('value');
  if (adminSnap.val() !== true) {
    throw new functions.https.HttpsError('permission-denied', 'Must be an admin.');
  }

  const { title, body } = data;
  if (!title || !body) {
    throw new functions.https.HttpsError('invalid-argument', 'Missing title or body.');
  }

  try {
    const result = await sendNotificationToAll(title, body);
    return {
      message: 'Notification sent',
      successCount: result.successCount,
      failureCount: result.failureCount
    };
  } catch (error) {
    console.error('Error sending notification:', error);
    throw new functions.https.HttpsError('internal', error.message);
  }
});

// ── Automated: Notify when scoring opens or closes ──
exports.notifyRoundStatus = functions.database
  .ref('roundStatus/{weekNum}')
  .onUpdate(async (change, context) => {
    const newStatus = change.after.val();
    const oldStatus = change.before.val();
    const weekNum = context.params.weekNum;

    if (oldStatus !== 'open' && newStatus === 'open') {
      // Get course name
      let courseName = '';
      try {
        const snap = await admin.database().ref('schedule/' + weekNum).once('value');
        courseName = (snap.val() || {}).course || '';
      } catch (e) { /* ignore */ }

      await sendNotificationToAll(
        'Scoring is Now Open! ⛳',
        `Live scoring is open for Week ${weekNum}${courseName ? ' at ' + courseName : ''}. Enter your scores!`
      );
    }

    if (oldStatus === 'open' && newStatus === 'closed') {
      await sendNotificationToAll(
        'Round Complete! 🏆',
        `Week ${weekNum} scoring is closed. Check the results and payouts!`
      );
    }

    return null;
  });
