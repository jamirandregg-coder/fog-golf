package golf.thefog.twa;

import android.content.pm.ActivityInfo;
import android.net.Uri;
import android.os.Bundle;

import androidx.browser.customtabs.CustomTabColorSchemeParams;
import androidx.browser.trusted.TrustedWebActivityIntentBuilder;
import androidx.browser.trusted.TwaLauncher;

/**
 * Launches the FOG Golf PWA as a Trusted Web Activity.
 * The app loads https://thefog.golf in full-screen mode (no browser UI).
 * Any changes pushed to Firebase Hosting appear instantly — no app update needed.
 */
public class LauncherActivity extends android.app.Activity {

    private static final Uri LAUNCH_URI = Uri.parse("https://thefog.golf");
    private static final int STATUS_BAR_COLOR = 0xFF0F0A10;
    private static final int NAVIGATION_BAR_COLOR = 0xFF0F0A10;

    private TwaLauncher mTwaLauncher;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        CustomTabColorSchemeParams colorScheme = new CustomTabColorSchemeParams.Builder()
                .setToolbarColor(STATUS_BAR_COLOR)
                .setNavigationBarColor(NAVIGATION_BAR_COLOR)
                .build();

        TrustedWebActivityIntentBuilder builder = new TrustedWebActivityIntentBuilder(LAUNCH_URI)
                .setDefaultColorSchemeParams(colorScheme)
                .setScreenOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        mTwaLauncher = new TwaLauncher(this);
        mTwaLauncher.launch(builder, null, null);
        finish();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (mTwaLauncher != null) {
            mTwaLauncher.destroy();
        }
    }
}
