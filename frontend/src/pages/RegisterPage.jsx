import { useState, useEffect, useRef } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/feedback/Toast';
import { validators, validate } from '../utils/validators';

export default function RegisterPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { register, verifyOTP, resendOTP } = useAuth();
  const toast = useToast();

  // Step state: 'form' or 'otp'
  const initialStep = searchParams.get('step') === 'otp' && searchParams.get('email') ? 'otp' : 'form';
  const [step, setStep] = useState(initialStep);
  const [registeredEmail, setRegisteredEmail] = useState(searchParams.get('email') || '');

  // Registration Form State
  const [formData, setFormData] = useState({
    username: '',
    display_name: '',
    email: searchParams.get('email') || '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // OTP State (6 digits)
  const [otpDigits, setOtpDigits] = useState(['', '', '', '', '', '']);
  const [otpError, setOtpError] = useState('');
  const [isVerifying, setIsVerifying] = useState(false);
  const [resendCooldown, setResendCooldown] = useState(60);
  const [isResending, setIsResending] = useState(false);
  const inputRefs = useRef([]);

  // Resend Countdown Timer
  useEffect(() => {
    if (step !== 'otp' || resendCooldown <= 0) return;
    const timer = setInterval(() => {
      setResendCooldown((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, [step, resendCooldown]);

  // Focus first OTP input on step change
  useEffect(() => {
    if (step === 'otp' && inputRefs.current[0]) {
      inputRefs.current[0].focus();
    }
  }, [step]);

  // Handle Form Change
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: null }));
    }
    if (serverError) setServerError('');
  };

  // Step 1: Submit Registration Form
  const handleRegisterSubmit = async (e) => {
    e.preventDefault();

    const usernameError = validate(formData.username, validators.required, validators.username);
    const emailError = validate(formData.email, validators.required, validators.email);
    const passwordError = validate(formData.password, validators.required, validators.password);
    const confirmError = validate(
      formData.confirmPassword,
      validators.required,
      validators.passwordsMatch(formData.password)
    );

    if (usernameError || emailError || passwordError || confirmError) {
      setErrors({
        username: usernameError,
        email: emailError,
        password: passwordError,
        confirmPassword: confirmError,
      });
      return;
    }

    setIsSubmitting(true);
    setServerError('');

    try {
      const res = await register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        display_name: formData.display_name,
      });

      if (res?.otp_required) {
        setRegisteredEmail(formData.email);
        setStep('otp');
        setResendCooldown(60);
        setOtpDigits(['', '', '', '', '', '']);
        toast.info('Verification code sent to your email!');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      const data = err?.response?.data;
      if (typeof data === 'object') {
        const firstKey = Object.keys(data)[0];
        const val = data[firstKey];
        const msg = Array.isArray(val) ? val[0] : (typeof val === 'string' ? val : 'Registration failed.');
        setServerError(`${firstKey !== 'detail' ? `${firstKey}: ` : ''}${msg}`);
      } else {
        setServerError('Unable to create account. Please try again later.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  // Step 2: Handle OTP Digit Input
  const handleOtpChange = (index, value) => {
    if (otpError) setOtpError('');

    // Handle full 6-digit paste
    if (value.length > 1) {
      const pasted = value.replace(/\D/g, '').slice(0, 6).split('');
      const newDigits = [...otpDigits];
      pasted.forEach((char, i) => {
        if (i < 6) newDigits[i] = char;
      });
      setOtpDigits(newDigits);
      const nextFocus = Math.min(pasted.length, 5);
      inputRefs.current[nextFocus]?.focus();
      return;
    }

    // Single digit input
    const cleanDigit = value.replace(/\D/g, '');
    const newDigits = [...otpDigits];
    newDigits[index] = cleanDigit;
    setOtpDigits(newDigits);

    // Auto-advance to next input
    if (cleanDigit && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  // Handle Backspace navigation
  const handleOtpKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !otpDigits[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  // Step 2: Verify OTP Submit
  const handleVerifySubmit = async (e) => {
    e.preventDefault();
    const fullOtp = otpDigits.join('');

    if (fullOtp.length !== 6) {
      setOtpError('Please enter the full 6-digit verification code.');
      return;
    }

    setIsVerifying(true);
    setOtpError('');

    try {
      await verifyOTP({
        email: registeredEmail,
        otp: fullOtp,
      });
      toast.success('Email verified successfully! Welcome to SkillForge.');
      navigate('/dashboard');
    } catch (err) {
      const msg = err?.response?.data?.detail || 'Invalid verification code. Please try again.';
      setOtpError(msg);
    } finally {
      setIsVerifying(false);
    }
  };

  // Step 2: Resend OTP
  const handleResendOtp = async () => {
    if (resendCooldown > 0 || isResending) return;

    setIsResending(true);
    setOtpError('');

    try {
      await resendOTP({ email: registeredEmail });
      setResendCooldown(60);
      setOtpDigits(['', '', '', '', '', '']);
      inputRefs.current[0]?.focus();
      toast.success('A new verification code has been sent to your email.');
    } catch (err) {
      const msg = err?.response?.data?.detail || 'Failed to resend verification code.';
      setOtpError(msg);
    } finally {
      setIsResending(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-12rem)] px-4 py-8">
      <div className="w-full max-w-lg bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-8 shadow-2xl">

        {/* ---------------- STEP 1: REGISTRATION FORM ---------------- */}
        {step === 'form' && (
          <>
            <div className="text-center mb-8">
              <h2 className="text-3xl font-extrabold text-white tracking-tight">Create Your Account</h2>
              <p className="text-sm text-[var(--color-text-secondary)] mt-2">
                Join SkillForge to master algorithms, build portfolio projects, and level up.
              </p>
            </div>

            {serverError && (
              <div className="mb-6 p-4 rounded-xl bg-red-950/60 border border-red-800 text-red-300 text-sm flex items-center gap-3">
                <svg className="w-5 h-5 flex-shrink-0 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                <span>{serverError}</span>
              </div>
            )}

            <form onSubmit={handleRegisterSubmit} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-1.5">
                    Username <span className="text-red-400">*</span>
                  </label>
                  <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    placeholder="e.g. dev_sarah"
                    className={`w-full px-4 py-2.5 rounded-xl bg-[var(--color-surface-dark)] border ${errors.username ? 'border-red-500 ring-1 ring-red-500' : 'border-[var(--color-surface-hover)] focus:border-[var(--color-brand-primary)] focus:ring-1 focus:ring-[var(--color-brand-primary)]'
                      } text-white placeholder-slate-500 text-sm transition outline-none`}
                  />
                  {errors.username && <p className="mt-1 text-xs text-red-400">{errors.username}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-1.5">
                    Display Name (Optional)
                  </label>
                  <input
                    type="text"
                    name="display_name"
                    value={formData.display_name}
                    onChange={handleChange}
                    placeholder="e.g. Sarah Connor"
                    className="w-full px-4 py-2.5 rounded-xl bg-[var(--color-surface-dark)] border border-[var(--color-surface-hover)] focus:border-[var(--color-brand-primary)] focus:ring-1 focus:ring-[var(--color-brand-primary)] text-white placeholder-slate-500 text-sm transition outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-1.5">
                  Email Address <span className="text-red-400">*</span>
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="sarah@example.com"
                  className={`w-full px-4 py-2.5 rounded-xl bg-[var(--color-surface-dark)] border ${errors.email ? 'border-red-500 ring-1 ring-red-500' : 'border-[var(--color-surface-hover)] focus:border-[var(--color-brand-primary)] focus:ring-1 focus:ring-[var(--color-brand-primary)]'
                    } text-white placeholder-slate-500 text-sm transition outline-none`}
                />
                {errors.email && <p className="mt-1 text-xs text-red-400">{errors.email}</p>}
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-1.5">
                    Password <span className="text-red-400">*</span>
                  </label>
                  <div className="relative">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      placeholder="Min 8 characters"
                      className={`w-full px-4 py-2.5 rounded-xl bg-[var(--color-surface-dark)] border ${errors.password ? 'border-red-500 ring-1 ring-red-500' : 'border-[var(--color-surface-hover)] focus:border-[var(--color-brand-primary)] focus:ring-1 focus:ring-[var(--color-brand-primary)]'
                        } text-white placeholder-slate-500 text-sm transition outline-none pr-10`}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200 transition"
                      aria-label="Toggle password visibility"
                    >
                      {showPassword ? (
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18" />
                        </svg>
                      ) : (
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                      )}
                    </button>
                  </div>
                  {errors.password && <p className="mt-1 text-xs text-red-400">{errors.password}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-1.5">
                    Confirm Password <span className="text-red-400">*</span>
                  </label>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    placeholder="Re-enter password"
                    className={`w-full px-4 py-2.5 rounded-xl bg-[var(--color-surface-dark)] border ${errors.confirmPassword ? 'border-red-500 ring-1 ring-red-500' : 'border-[var(--color-surface-hover)] focus:border-[var(--color-brand-primary)] focus:ring-1 focus:ring-[var(--color-brand-primary)]'
                      } text-white placeholder-slate-500 text-sm transition outline-none`}
                  />
                  {errors.confirmPassword && <p className="mt-1 text-xs text-red-400">{errors.confirmPassword}</p>}
                </div>
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full mt-2 py-3 px-4 rounded-xl bg-[var(--color-brand-primary)] hover:bg-[var(--color-brand-primary-hover)] text-white font-semibold text-sm transition shadow-lg shadow-indigo-500/25 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Sending Verification Code...
                  </>
                ) : (
                  'Create Account'
                )}
              </button>
            </form>

            <div className="mt-8 pt-6 border-t border-[var(--color-surface-hover)] text-center text-sm text-[var(--color-text-secondary)]">
              Already have an account?{' '}
              <Link to="/login" className="text-[var(--color-brand-accent)] hover:underline font-medium">
                Sign in
              </Link>
            </div>
          </>
        )}

        {/* ---------------- STEP 2: OTP VERIFICATION SCREEN ---------------- */}
        {step === 'otp' && (
          <div className="text-center">
            {/* Header Icon */}
            <div className="mx-auto w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mb-6">
              <svg className="w-8 h-8 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>

            <h2 className="text-3xl font-extrabold text-white tracking-tight">Verify Your Email</h2>
            <p className="text-sm text-[var(--color-text-secondary)] mt-2">
              We sent a 6-digit verification code to
            </p>
            <p className="text-sm font-semibold text-indigo-300 mt-0.5">
              {registeredEmail}
            </p>

            {otpError && (
              <div className="mt-6 p-4 rounded-xl bg-red-950/60 border border-red-800 text-red-300 text-sm flex items-center gap-3 text-left">
                <svg className="w-5 h-5 flex-shrink-0 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                <span>{otpError}</span>
              </div>
            )}

            {/* 6 Digit Input Boxes */}
            <form onSubmit={handleVerifySubmit} className="mt-8 space-y-6">
              <div className="flex justify-center gap-2 sm:gap-3">
                {otpDigits.map((digit, idx) => (
                  <input
                    key={idx}
                    ref={(el) => (inputRefs.current[idx] = el)}
                    type="text"
                    inputMode="numeric"
                    maxLength={6}
                    value={digit}
                    onChange={(e) => handleOtpChange(idx, e.target.value)}
                    onKeyDown={(e) => handleOtpKeyDown(idx, e)}
                    className={`w-11 h-13 sm:w-13 sm:h-15 text-center text-xl sm:text-2xl font-bold rounded-xl bg-[var(--color-surface-dark)] border ${otpError
                        ? 'border-red-500 ring-1 ring-red-500'
                        : digit
                          ? 'border-indigo-500 ring-1 ring-indigo-500/50 text-white'
                          : 'border-[var(--color-surface-hover)] focus:border-[var(--color-brand-primary)] focus:ring-1 focus:ring-[var(--color-brand-primary)] text-white'
                      } transition outline-none`}
                  />
                ))}
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isVerifying || otpDigits.join('').length !== 6}
                className="w-full py-3 px-4 rounded-xl bg-[var(--color-brand-primary)] hover:bg-[var(--color-brand-primary-hover)] text-white font-semibold text-sm transition shadow-lg shadow-indigo-500/25 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isVerifying ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Verifying Code...
                  </>
                ) : (
                  'Verify & Activate Account'
                )}
              </button>
            </form>

            {/* Resend Code Section */}
            <div className="mt-6 flex flex-col items-center gap-2 text-sm text-[var(--color-text-secondary)]">
              {resendCooldown > 0 ? (
                <p className="text-slate-400">
                  Resend code in <span className="font-semibold text-indigo-400">{resendCooldown}s</span>
                </p>
              ) : (
                <button
                  type="button"
                  onClick={handleResendOtp}
                  disabled={isResending}
                  className="text-indigo-400 hover:text-indigo-300 font-semibold transition hover:underline"
                >
                  {isResending ? 'Sending...' : 'Resend Verification Code'}
                </button>
              )}

              <button
                type="button"
                onClick={() => {
                  setStep('form');
                  setOtpError('');
                }}
                className="mt-2 text-xs text-slate-500 hover:text-slate-300 transition"
              >
                ← Back to registration / Change email
              </button>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
