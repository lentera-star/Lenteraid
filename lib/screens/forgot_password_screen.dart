import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:lentera/auth/supabase_auth_manager.dart';
import 'package:lentera/theme.dart';

class ForgotPasswordScreen extends StatefulWidget {
  const ForgotPasswordScreen({super.key});

  @override
  State<ForgotPasswordScreen> createState() => _ForgotPasswordScreenState();
}

class _ForgotPasswordScreenState extends State<ForgotPasswordScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _auth = SupabaseAuthManager();
  bool _sending = false;

  @override
  void dispose() {
    _emailController.dispose();
    super.dispose();
  }

  Future<void> _sendReset() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _sending = true);
    await _auth.resetPassword(email: _emailController.text.trim(), context: context);
    if (mounted) setState(() => _sending = false);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Lupa Password'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          color: colors.onSurface,
          onPressed: () => context.pop(),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: AppSpacing.paddingLg,
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 12),
                Icon(Icons.lock_reset, size: 72, color: colors.primary),
                const SizedBox(height: 16),
                Text(
                  'Atur Ulang Kata Sandi',
                  style: theme.textTheme.titleLarge?.semiBold,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  'Masukkan email yang terdaftar. Kami akan mengirim tautan untuk mengatur ulang kata sandi Anda.',
                  style: theme.textTheme.bodyMedium?.withColor(colors.onSurface.withValues(alpha: 0.7)),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 28),
                TextFormField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  autofillHints: const [AutofillHints.email],
                  decoration: InputDecoration(
                    labelText: 'Email',
                    prefixIcon: const Icon(Icons.email_outlined, color: Colors.blue),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(AppRadius.md)),
                  ),
                  validator: (value) {
                    final v = value?.trim() ?? '';
                    if (v.isEmpty) return 'Email tidak boleh kosong';
                    if (!v.contains('@')) return 'Email tidak valid';
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                FilledButton.icon(
                  onPressed: _sending ? null : _sendReset,
                  style: FilledButton.styleFrom(padding: const EdgeInsets.symmetric(vertical: 14)),
                  icon: _sending
                      ? const SizedBox(height: 18, width: 18, child: CircularProgressIndicator(strokeWidth: 2))
                      : const Icon(Icons.send_outlined, color: Colors.white),
                  label: Text(_sending ? 'Mengirim...' : 'Kirim Tautan Reset',
                      style: theme.textTheme.labelLarge?.withColor(colors.onPrimary)),
                ),
                const SizedBox(height: 12),
                TextButton.icon(
                  onPressed: _sending ? null : () => context.go('/login'),
                  icon: const Icon(Icons.login, color: Colors.blue),
                  label: const Text('Kembali ke Masuk'),
                ),
                const SizedBox(height: 8),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: colors.surfaceContainerHighest,
                    borderRadius: BorderRadius.circular(AppRadius.md),
                  ),
                  child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    const Icon(Icons.info_outline, color: Colors.blue),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        'Jika Anda tidak menerima email dalam 2–3 menit, cek folder Spam/Promotions.',
                        style: theme.textTheme.bodySmall,
                      ),
                    ),
                  ]),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
