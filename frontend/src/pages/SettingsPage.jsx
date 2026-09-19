import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/feedback/Toast';
import { accountService } from '../services/api/accountService';
import Spinner from '../components/feedback/Spinner';

const PRESET_AVATARS = [
  'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
  'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
  'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80',
  'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150&auto=format&fit=crop&q=80',
  'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150&auto=format&fit=crop&q=80',
  'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=150&auto=format&fit=crop&q=80',
];

export default function SettingsPage() {
  const { user, refreshUser } = useAuth();
  const toast = useToast();
  const [activeTab, setActiveTab] = useState('profile'); // 'profile' | 'security'

  // Email change modal state
  const [isEmailModalOpen, setIsEmailModalOpen] = useState(false);
  const [emailStep, setEmailStep] = useState('request'); // 'request' | 'confirm'
  const [newEmail, setNewEmail] = useState('');
  const [currentPassword, setCurrentPassword] = useState('');
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [emailOtpDigits, setEmailOtpDigits] = useState(['', '', '', '', '', '']);
  const [emailChangeLoading, setEmailChangeLoading] = useState(false);
  const [emailChangeError, setEmailChangeError] = useState('');
  const [emailResendCooldown, setEmailResendCooldown] = useState(60);
  const emailOtpRefs = useRef([]);

  // Profile form state
  const [profileForm, setProfileForm] = useState({
    display_name: '',
    username: '',
    email: '',
    phone_number: '',
    bio: '',
    location: '',
    avatar_url: '',
    github_url: '',
    linkedin_url: '',
    twitter_url: '',
    website_url: '',
  });

  const [profileSaving, setProfileSaving] = useState(false);
  const [profileSuccess, setProfileSuccess] = useState('');
  const [profileError, setProfileError] = useState('');

  // Password form state
  const [passwordForm, setPasswordForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  });

  const [passwordSaving, setPasswordSaving] = useState(false);
  const [passwordSuccess, setPasswordSuccess] = useState('');
  const [passwordError, setPasswordError] = useState('');

  // Initialize form from user context
  useEffect(() => {
    if (user) {
      setProfileForm({
        display_name: user.profile?.display_name || '',
        username: user.username || '',
        email: user.email || '',
        phone_number: user.profile?.phone_number || '',
        bio: user.profile?.bio || '',
        location: user.profile?.location || '',
        avatar_url: user.profile?.avatar_url || '',
        github_url: user.profile?.github_url || '',
        linkedin_url: user.profile?.linkedin_url || '',
        twitter_url: user.profile?.twitter_url || '',
        website_url: user.profile?.website_url || '',
      });
    }
  }, [user]);

  // Cooldown timer for email change OTP
  useEffect(() => {
    if (!isEmailModalOpen || emailStep !== 'confirm' || emailResendCooldown <= 0) return;
    const timer = setInterval(() => {
      setEmailResendCooldown((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, [isEmailModalOpen, emailStep, emailResendCooldown]);

  const openEmailModal = () => {
    setIsEmailModalOpen(true);
    setEmailStep('request');
    setNewEmail('');
    setCurrentPassword('');
    setEmailOtpDigits(['', '', '', '', '', '']);
    setEmailChangeError('');
    setEmailResendCooldown(60);
  };

  const closeEmailModal = () => {
    setIsEmailModalOpen(false);
    setEmailChangeError('');
  };

  const handleRequestEmailChange = async (e) => {
    e.preventDefault();
    if (!newEmail || !currentPassword) {
      setEmailChangeError('Please enter both your new email and current password.');
      return;
    }
    setEmailChangeLoading(true);
    setEmailChangeError('');

    try {
      await accountService.requestEmailChange({
        new_email: newEmail,
        current_password: currentPassword,
      });
      setEmailStep('confirm');
      setEmailResendCooldown(60);
      setEmailOtpDigits(['', '', '', '', '', '']);
      toast.info(`Verification code sent to ${newEmail}`);
      setTimeout(() => emailOtpRefs.current[0]?.focus(), 100);
    } catch (err) {
      const detail =
        err?.response?.data?.detail ||
        err?.response?.data?.current_password?.[0] ||
        err?.response?.data?.new_email?.[0] ||
        'Failed to request email change.';
      setEmailChangeError(detail);
    } finally {
      setEmailChangeLoading(false);
    }
  };

  const handleEmailOtpChange = (index, value) => {
    if (emailChangeError) setEmailChangeError('');

    // Handle paste
    if (value.length > 1) {
      const pasted = value.replace(/\D/g, '').slice(0, 6).split('');
      const newDigits = [...emailOtpDigits];
      pasted.forEach((char, i) => {
        if (i < 6) newDigits[i] = char;
      });
      setEmailOtpDigits(newDigits);
      const nextFocus = Math.min(pasted.length, 5);
      emailOtpRefs.current[nextFocus]?.focus();
      return;
    }

    const cleanDigit = value.replace(/\D/g, '');
    const newDigits = [...emailOtpDigits];
    newDigits[index] = cleanDigit;
    setEmailOtpDigits(newDigits);

    if (cleanDigit && index < 5) {
      emailOtpRefs.current[index + 1]?.focus();
    }
  };

  const handleEmailOtpKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !emailOtpDigits[index] && index > 0) {
      emailOtpRefs.current[index - 1]?.focus();
    }
  };

  const handleConfirmEmailChange = async (e) => {
    e.preventDefault();
    const otp = emailOtpDigits.join('');
    if (otp.length !== 6) {
      setEmailChangeError('Please enter the full 6-digit code.');
      return;
    }

    setEmailChangeLoading(true);
    setEmailChangeError('');

    try {
      const res = await accountService.confirmEmailChange({
        new_email: newEmail,
        otp,
      });
      toast.success('Email updated successfully! Security alert sent to your previous email.');
      setProfileForm((prev) => ({ ...prev, email: res?.email || newEmail }));
      if (refreshUser) refreshUser();
      closeEmailModal();
    } catch (err) {
      const detail = err?.response?.data?.detail || err?.response?.data?.otp?.[0] || 'Failed to confirm email change.';
      setEmailChangeError(detail);
    } finally {
      setEmailChangeLoading(false);
    }
  };

  const handleResendEmailChangeOtp = async () => {
    if (emailResendCooldown > 0 || emailChangeLoading) return;
    setEmailChangeLoading(true);
    setEmailChangeError('');

    try {
      await accountService.requestEmailChange({
        new_email: newEmail,
        current_password: currentPassword,
      });
      setEmailResendCooldown(60);
      setEmailOtpDigits(['', '', '', '', '', '']);
      emailOtpRefs.current[0]?.focus();
      toast.info('New verification code sent!');
    } catch (err) {
      const detail = err?.response?.data?.detail || 'Failed to resend code.';
      setEmailChangeError(detail);
    } finally {
      setEmailChangeLoading(false);
    }
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setProfileSaving(true);
    setProfileSuccess('');
    setProfileError('');

    try {
      const { email, ...profileData } = profileForm;
      await accountService.updateProfile(profileData);
      setProfileSuccess('Profile updated successfully!');
      if (refreshUser) refreshUser();
      setTimeout(() => setProfileSuccess(''), 4000);
    } catch (err) {
      console.error('Failed to update profile:', err);
      const detail = err?.response?.data?.detail;
      if (typeof detail === 'object') {
        const firstKey = Object.keys(detail)[0];
        setProfileError(`${firstKey}: ${detail[firstKey]}`);
      } else {
        setProfileError(detail || 'Failed to update profile. Please try again.');
      }
    } finally {
      setProfileSaving(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    if (passwordForm.new_password !== passwordForm.confirm_password) {
      setPasswordError('New passwords do not match.');
      return;
    }

    setPasswordSaving(true);
    setPasswordSuccess('');
    setPasswordError('');

    try {
      await accountService.changePassword(passwordForm);
      setPasswordSuccess('Password changed successfully!');
      setPasswordForm({
        current_password: '',
        new_password: '',
        confirm_password: '',
      });
      setTimeout(() => setPasswordSuccess(''), 4000);
    } catch (err) {
      console.error('Failed to change password:', err);
      const detail = err?.response?.data?.detail;
      if (typeof detail === 'object') {
        const firstKey = Object.keys(detail)[0];
        setPasswordError(`${firstKey}: ${detail[firstKey]}`);
      } else {
        setPasswordError(detail || 'Failed to change password. Check your current password.');
      }
    } finally {
      setPasswordSaving(false);
    }
  };

  return (
    <div className="w-full min-w-0 max-w-4xl mx-auto space-y-8 pb-24">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            <span>⚙️</span> Account Settings
          </h1>
          <p className="text-slate-400 text-xs sm:text-sm mt-1">
            Manage your developer profile, identity, social links, and security credentials.
          </p>
        </div>

        {user && (
          <Link
            to={`/portfolio/${user.username}`}
            className="px-4 py-2 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-white text-xs font-semibold border border-slate-700/60 shadow-sm transition flex items-center gap-2 self-start sm:self-auto"
          >
            <span>👨‍💻</span>
            <span>View Public Profile</span>
          </Link>
        )}
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800">
        <button
          onClick={() => setActiveTab('profile')}
          className={`pb-3 px-4 text-xs font-bold font-mono transition-all border-b-2 flex items-center gap-2 ${activeTab === 'profile'
            ? 'border-indigo-500 text-white'
            : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
        >
          <span>👤</span> Profile Information
        </button>

        <button
          onClick={() => setActiveTab('security')}
          className={`pb-3 px-4 text-xs font-bold font-mono transition-all border-b-2 flex items-center gap-2 ${activeTab === 'security'
            ? 'border-indigo-500 text-white'
            : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
        >
          <span>🔒</span> Security & Password
        </button>
      </div>

      {/* Tab 1: Profile Information */}
      {activeTab === 'profile' && (
        <form onSubmit={handleProfileSubmit} className="space-y-6">
          {profileSuccess && (
            <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold flex items-center gap-2">
              <span>✓</span> {profileSuccess}
            </div>
          )}

          {profileError && (
            <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-semibold flex items-center gap-2">
              <span>⚠️</span> {profileError}
            </div>
          )}

          {/* Avatar Section */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4">
            <h2 className="text-sm font-bold text-white uppercase font-mono tracking-wider">
              Profile Picture / Avatar
            </h2>

            <div className="flex flex-col sm:flex-row items-center gap-6">
              {/* Avatar Preview */}
              <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-indigo-600 to-cyan-400 flex items-center justify-center text-3xl font-black text-white shadow-md overflow-hidden flex-shrink-0 border-2 border-slate-700">
                {profileForm.avatar_url ? (
                  <img
                    src={profileForm.avatar_url}
                    alt="Preview"
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                ) : (
                  profileForm.display_name?.charAt(0)?.toUpperCase() || profileForm.username?.charAt(0)?.toUpperCase() || 'U'
                )}
              </div>

              <div className="flex-1 space-y-3 w-full">
                <div>
                  <label className="block text-xs font-mono text-slate-400 mb-1">
                    Custom Avatar Image URL
                  </label>
                  <input
                    type="url"
                    placeholder="https://example.com/avatar.jpg"
                    value={profileForm.avatar_url}
                    onChange={(e) => setProfileForm({ ...profileForm, avatar_url: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                  />
                </div>

                {/* Preset Avatars */}
                <div>
                  <span className="block text-[11px] font-mono text-slate-500 mb-1.5">
                    Or choose a preset avatar:
                  </span>
                  <div className="flex items-center gap-2.5 flex-wrap">
                    {PRESET_AVATARS.map((url, i) => (
                      <button
                        key={i}
                        type="button"
                        onClick={() => setProfileForm({ ...profileForm, avatar_url: url })}
                        className={`w-9 h-9 rounded-xl overflow-hidden border-2 transition-all ${profileForm.avatar_url === url
                          ? 'border-indigo-500 scale-105 shadow-md shadow-indigo-500/30'
                          : 'border-slate-800 opacity-70 hover:opacity-100 hover:border-slate-600'
                          }`}
                      >
                        <img src={url} alt={`Preset ${i + 1}`} className="w-full h-full object-cover" />
                      </button>
                    ))}
                    {profileForm.avatar_url && (
                      <button
                        type="button"
                        onClick={() => setProfileForm({ ...profileForm, avatar_url: '' })}
                        className="text-[11px] text-slate-400 hover:text-white underline ml-2"
                      >
                        Reset
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Personal Details */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4">
            <h2 className="text-sm font-bold text-white uppercase font-mono tracking-wider">
              Personal Information
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  Display Name
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Alex River"
                  value={profileForm.display_name}
                  onChange={(e) => setProfileForm({ ...profileForm, display_name: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  Username
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. alexriver"
                  value={profileForm.username}
                  onChange={(e) => setProfileForm({ ...profileForm, username: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 font-mono"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  Email Address
                </label>
                <div className="flex items-center justify-between bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2">
                  <div className="flex items-center gap-2 min-w-0">
                    <span className="text-xs text-white truncate font-mono">{profileForm.email}</span>
                    <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex-shrink-0">
                      ✓ Verified
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={openEmailModal}
                    className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 transition hover:underline ml-3 flex-shrink-0"
                  >
                    Change Email
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  Contact / Phone Number
                </label>
                <input
                  type="tel"
                  placeholder="e.g. +1 (555) 234-5678"
                  value={profileForm.phone_number}
                  onChange={(e) => setProfileForm({ ...profileForm, phone_number: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="sm:col-span-2">
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  Location / Timezone
                </label>
                <input
                  type="text"
                  placeholder="e.g. San Francisco, CA (UTC-8)"
                  value={profileForm.location}
                  onChange={(e) => setProfileForm({ ...profileForm, location: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="sm:col-span-2">
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  Bio / Professional Summary
                </label>
                <textarea
                  rows={3}
                  placeholder="Tell other developers about your engineering experience, favorite languages, and projects..."
                  value={profileForm.bio}
                  onChange={(e) => setProfileForm({ ...profileForm, bio: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 leading-relaxed"
                />
              </div>
            </div>
          </div>

          {/* Social & Professional Links */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4">
            <h2 className="text-sm font-bold text-white uppercase font-mono tracking-wider">
              Social & Professional Links
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  GitHub Profile URL
                </label>
                <input
                  type="url"
                  placeholder="https://github.com/username"
                  value={profileForm.github_url}
                  onChange={(e) => setProfileForm({ ...profileForm, github_url: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  LinkedIn Profile URL
                </label>
                <input
                  type="url"
                  placeholder="https://linkedin.com/in/username"
                  value={profileForm.linkedin_url}
                  onChange={(e) => setProfileForm({ ...profileForm, linkedin_url: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  Twitter / X Profile URL
                </label>
                <input
                  type="url"
                  placeholder="https://x.com/username"
                  value={profileForm.twitter_url}
                  onChange={(e) => setProfileForm({ ...profileForm, twitter_url: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  Portfolio / Personal Website URL
                </label>
                <input
                  type="url"
                  placeholder="https://yourportfolio.dev"
                  value={profileForm.website_url}
                  onChange={(e) => setProfileForm({ ...profileForm, website_url: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={profileSaving}
              className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-md shadow-indigo-600/30 transition disabled:opacity-50 flex items-center gap-2"
            >
              {profileSaving ? (
                <>
                  <Spinner size="sm" />
                  <span>Saving Changes...</span>
                </>
              ) : (
                <>
                  <span>Save Profile Changes</span>
                  <span>➔</span>
                </>
              )}
            </button>
          </div>
        </form>
      )}

      {/* Tab 2: Security & Password */}
      {activeTab === 'security' && (
        <form onSubmit={handlePasswordSubmit} className="space-y-6 max-w-xl">
          {passwordSuccess && (
            <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold flex items-center gap-2">
              <span>✓</span> {passwordSuccess}
            </div>
          )}

          {passwordError && (
            <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-semibold flex items-center gap-2">
              <span>⚠️</span> {passwordError}
            </div>
          )}

          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4">
            <h2 className="text-sm font-bold text-white uppercase font-mono tracking-wider">
              Change Password
            </h2>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  Current Password
                </label>
                <input
                  type="password"
                  required
                  value={passwordForm.current_password}
                  onChange={(e) => setPasswordForm({ ...passwordForm, current_password: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  New Password (min 8 characters)
                </label>
                <input
                  type="password"
                  required
                  minLength={8}
                  value={passwordForm.new_password}
                  onChange={(e) => setPasswordForm({ ...passwordForm, new_password: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  Confirm New Password
                </label>
                <input
                  type="password"
                  required
                  minLength={8}
                  value={passwordForm.confirm_password}
                  onChange={(e) => setPasswordForm({ ...passwordForm, confirm_password: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={passwordSaving}
              className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-md shadow-indigo-600/30 transition disabled:opacity-50 flex items-center gap-2"
            >
              {passwordSaving ? (
                <>
                  <Spinner size="sm" />
                  <span>Updating Password...</span>
                </>
              ) : (
                <>
                  <span>Update Password</span>
                  <span>➔</span>
                </>
              )}
            </button>
          </div>
        </form>
      )}

      {/* Email Change Modal */}
      {isEmailModalOpen && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in"
          role="dialog"
          aria-modal="true"
        >
          <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <span>✉️</span> Change Account Email
              </h3>
              <button
                type="button"
                onClick={closeEmailModal}
                className="text-slate-400 hover:text-white text-lg transition"
              >
                ✕
              </button>
            </div>

            {emailChangeError && (
              <div className="p-3 rounded-xl bg-red-950/60 border border-red-800 text-red-300 text-xs flex items-center gap-2">
                <span>⚠️</span> {emailChangeError}
              </div>
            )}

            {emailStep === 'request' ? (
              <form onSubmit={handleRequestEmailChange} className="space-y-4">
                <p className="text-xs text-slate-400 leading-relaxed">
                  For your security, enter your current password and your new email address. A 6-digit verification code will be sent to the new email.
                </p>

                <div>
                  <label className="block text-xs font-mono text-slate-400 mb-1">Current Email</label>
                  <input
                    type="text"
                    disabled
                    value={profileForm.email}
                    className="w-full bg-slate-950/50 border border-slate-800/80 rounded-xl px-3.5 py-2 text-xs text-slate-500 cursor-not-allowed font-mono"
                  />
                </div>

                <div>
                  <label className="block text-xs font-mono text-slate-400 mb-1">
                    New Email Address <span className="text-red-400">*</span>
                  </label>
                  <input
                    type="email"
                    required
                    placeholder="newemail@example.com"
                    value={newEmail}
                    onChange={(e) => setNewEmail(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 font-mono"
                  />
                </div>

                <div>
                  <label className="block text-xs font-mono text-slate-400 mb-1">
                    Current Password <span className="text-red-400">*</span>
                  </label>
                  <div className="relative">
                    <input
                      type={showCurrentPassword ? 'text' : 'password'}
                      required
                      placeholder="Enter your account password"
                      value={currentPassword}
                      onChange={(e) => setCurrentPassword(e.target.value)}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 pr-12 font-mono"
                    />
                    <button
                      type="button"
                      onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200 text-xs font-mono"
                    >
                      {showCurrentPassword ? 'Hide' : 'Show'}
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-end gap-3 pt-2">
                  <button
                    type="button"
                    onClick={closeEmailModal}
                    className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={emailChangeLoading || !newEmail || !currentPassword}
                    className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition disabled:opacity-50 flex items-center gap-2"
                  >
                    {emailChangeLoading ? 'Sending Code...' : 'Send Verification Code'}
                  </button>
                </div>
              </form>
            ) : (
              <form onSubmit={handleConfirmEmailChange} className="space-y-4">
                <div className="text-center space-y-1">
                  <p className="text-xs text-slate-400">We sent a 6-digit confirmation code to</p>
                  <p className="text-xs font-bold text-indigo-300 font-mono">{newEmail}</p>
                </div>

                <div className="flex justify-center gap-2 py-2">
                  {emailOtpDigits.map((digit, idx) => (
                    <input
                      key={idx}
                      ref={(el) => (emailOtpRefs.current[idx] = el)}
                      type="text"
                      inputMode="numeric"
                      maxLength={6}
                      value={digit}
                      onChange={(e) => handleEmailOtpChange(idx, e.target.value)}
                      onKeyDown={(e) => handleEmailOtpKeyDown(idx, e)}
                      className={`w-10 h-12 text-center text-lg font-bold rounded-xl bg-slate-950 border ${digit
                          ? 'border-indigo-500 ring-1 ring-indigo-500/50 text-white'
                          : 'border-slate-800 text-white focus:border-indigo-500'
                        } transition outline-none font-mono`}
                    />
                  ))}
                </div>

                <button
                  type="submit"
                  disabled={emailChangeLoading || emailOtpDigits.join('').length !== 6}
                  className="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition disabled:opacity-50"
                >
                  {emailChangeLoading ? 'Confirming...' : 'Confirm & Update Email'}
                </button>

                <div className="flex flex-col items-center gap-1.5 pt-2 text-[11px] text-slate-400">
                  {emailResendCooldown > 0 ? (
                    <p>
                      Resend code in <span className="text-indigo-400 font-mono">{emailResendCooldown}s</span>
                    </p>
                  ) : (
                    <button
                      type="button"
                      onClick={handleResendEmailChangeOtp}
                      disabled={emailChangeLoading}
                      className="text-indigo-400 hover:underline font-semibold"
                    >
                      Resend Verification Code
                    </button>
                  )}
                  <button
                    type="button"
                    onClick={() => {
                      setEmailStep('request');
                      setEmailChangeError('');
                    }}
                    className="text-slate-500 hover:text-slate-300 text-[10px] mt-1"
                  >
                    ← Back to edit email
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

