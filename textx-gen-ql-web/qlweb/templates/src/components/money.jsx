import InputLabel from '@mui/material/InputLabel';
import { styled } from '@mui/material/styles';
import CurrencyInput from 'react-currency-input-field';

const StyledRoot = styled('div')({
  position: 'relative',
  margin: '8px 0', // Match MUI TextField spacing
});

const StyledInputWrapper = styled('div')(({ theme, disabled }) => ({
  backgroundColor: disabled
    ? theme.palette.action.disabledBackground
    : theme.palette.grey[50], // Match MUI filled input bg
  borderTopLeftRadius: theme.shape.borderRadius,
  borderTopRightRadius: theme.shape.borderRadius,
  borderBottom: `1px solid ${theme.palette.divider}`,
  transition: theme.transitions.create('border-bottom-color'),
  '&:hover': {
    backgroundColor: disabled ? undefined : theme.palette.grey[100],
  },
  '&.Mui-focused': {
    borderBottom: `2px solid ${theme.palette.primary.main}`,
    backgroundColor: theme.palette.grey[100],
  },
}));

const StyledCurrencyInput = styled(CurrencyInput)(({ theme }) => ({
  width: '100%',
  padding: '25px 12px 8px', // Top padding for label, bottom for text
  font: 'inherit',
  border: 0,
  backgroundColor: 'transparent',
  '&:focus': {
    outline: 0,
  },
}));

const StyledLabel = styled(InputLabel)(({ theme }) => ({
  position: 'absolute',
  fontSize: '0.8rem',
  left: 12,
  top: 8, // Positions label inside input
  color: theme.palette.text.secondary,
  transform: 'none', // Prevents label scaling
  transition: theme.transitions.create(['top', 'color'], {
    duration: theme.transitions.duration.shorter,
  }),
  '&.Mui-focused, &.MuiFormLabel-filled': {
    color: theme.palette.primary.main,
  },
}));

export default function MoneyField({ name, label, value, onChange,
                                     disabled = false, prefix = '€', decimalPlaces = 2}) {
  return (
    <StyledRoot>
      <StyledInputWrapper
        className={value ? 'MuiFormLabel-filled' : ''}
        disabled={disabled}
      >
        <StyledLabel shrink disabled={disabled}>
          {label}
        </StyledLabel>
        <StyledCurrencyInput
          id={name}
          name={name}
          value={value}
          onValueChange={(val) => onChange(name, val)}
          decimalsLimit={decimalPlaces}
          prefix={prefix}
          disabled={disabled}
        />
      </StyledInputWrapper>
    </StyledRoot>
  );
}
