package golf.thefog.twa;

import android.content.ComponentName;
import android.content.pm.ActivityInfo;
import android.net.Uri;
import android.os.Bundle;

import androidx.browser.customtabs.CustomTabColorSchemeParams;
import androidx.browser.customtabs.CustomTabsClient;
import androidx.browser.customtabs.CustomTabsIntent;
import androidx.browser.customtabs.CustomTabsServiceConnection;
import androidx.browser.customtabs.CustomTabsSession;
import androidx.browser.trusted.TrustedWebActivityIntentBuilder;

/**
 * Launches the FOG Golf PWA as a Trusted Web Activity.
 * The app loads https://thefog.golf in full-screen mode (no browser UI).
 * Any changes pushed to Firebase Hosting appear instantly — no app update needed.
 */
public class LauncherActivity extends android.app.Activity {

    private static final Uri LAUNCH_URI = Uri.parse("https://thefog.golf");
    private static final int BG_COLOR = 0xFF0F0A10;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        CustomTabColorSchemeParams colorScheme = new CustomTabColorSchemeParams.Builder()
                .setToolbarColor(BG_COLOR)
                .setNavigationBarColor(BG_COLOR)
                .build();

        TrustedWebActivityIntentBuilder builder = new TrustedWebActivityIntentBuilder(LAUNCH_URI)
                .setDefaultColorSchemeParams(colorScheme)
                .setScreenOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        // Launch as a Custom Tab with TWA intent — Chrome will promote to
        // full-screen TWA automatically when Digital Asset Links verify.
        CustomTabsIntent intent = builder.buildCustomTabsIntent();
        intent.launchUrl(this, LAUNCH_URI);
        finish();
    }
}
