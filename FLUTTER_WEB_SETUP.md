# Flutter Web Development Configuration

## Fixed Port for OAuth Consistency

To run Flutter web with a fixed port (for consistent OAuth redirect URLs):

```bash
flutter run -d chrome --web-port 5500
```

## Why Fixed Port?

**Problem**: Flutter web uses random ports (4440, 23518, etc.) which causes `redirect_uri_mismatch` errors with Google OAuth.

**Solution**: Use `--web-port 5500` to always run on the same port.

## Google OAuth Configuration

### For Development (localhost)
Add to Google Cloud Console → Authorized redirect URIs:
```
http://localhost:5500/auth/v1/callback
```

### For Production
When deploying to production, add your production domain:
```
https://lentera.app/auth/v1/callback
https://ghtjooqihfvbmdaojpp.supabase.co/auth/v1/callback
```

## Production Deployment Strategy

### Option 1: Supabase Hosting (Recommended)
- Deploy Flutter web build to Supabase Storage
- Use Supabase domain: `https://ghtjooqihfvbmdaojpp.supabase.co`
- No CORS issues, seamless integration

### Option 2: Firebase Hosting
- `flutter build web --release`
- `firebase deploy --only hosting`
- Custom domain setup available

### Option 3: Vercel/Netlify
- Connect GitHub repo
- Auto-deploy on push
- Free SSL certificates

### OAuth Production Setup
1. Add production domain to Google Cloud Console
2. Update `supabase_auth_manager.dart`:
   ```dart
   redirectTo: kIsWeb 
       ? (kReleaseMode 
           ? 'https://your-domain.com/auth/v1/callback'
           : 'http://localhost:5500/auth/v1/callback')
       : 'io.lentera.app://login-callback'
   ```
3. Test OAuth flow in production environment

## Quick Commands

**Development**:
```bash
flutter run -d chrome --web-port 5500
```

**Build for Production**:
```bash
flutter build web --release
```

**Deploy to Firebase**:
```bash
flutter build web --release
firebase deploy --only hosting
```
