import { Box, LinearProgress, Typography } from '@mui/material';

interface PasswordStrengthIndicatorProps {
  password: string;
}

interface StrengthResult {
  score: number;
  label: string;
  color: 'error' | 'warning' | 'info' | 'success';
}

const calculatePasswordStrength = (password: string): StrengthResult => {
  let score = 0;

  if (!password) {
    return { score: 0, label: '', color: 'error' };
  }

  // Length check
  if (password.length >= 12) score += 25;
  else if (password.length >= 8) score += 15;

  // Uppercase check
  if (/[A-Z]/.test(password)) score += 20;

  // Lowercase check
  if (/[a-z]/.test(password)) score += 20;

  // Number check
  if (/\d/.test(password)) score += 20;

  // Special character check
  if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) score += 15;

  // Determine label and color
  if (score < 40) {
    return { score, label: 'Weak', color: 'error' };
  } else if (score < 60) {
    return { score, label: 'Fair', color: 'warning' };
  } else if (score < 80) {
    return { score, label: 'Good', color: 'info' };
  } else {
    return { score, label: 'Strong', color: 'success' };
  }
};

function PasswordStrengthIndicator({ password }: PasswordStrengthIndicatorProps) {
  const strength = calculatePasswordStrength(password);

  if (!password) {
    return null;
  }

  return (
    <Box sx={{ mt: 1 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 0.5 }}>
        <LinearProgress
          variant="determinate"
          value={strength.score}
          color={strength.color}
          sx={{ flexGrow: 1, height: 6, borderRadius: 3 }}
        />
        <Typography variant="caption" sx={{ minWidth: 60, textAlign: 'right' }}>
          {strength.label}
        </Typography>
      </Box>
      <Typography variant="caption" color="text.secondary">
        Use 12+ characters with mixed case, numbers, and symbols
      </Typography>
    </Box>
  );
}

export default PasswordStrengthIndicator;
