import TextField from '@mui/material/TextField';

export default function NumericField( { name, label, value, onChange, disabled = false} ) {
  return (
    <TextField
        name={name}
        label={label}
        variant="filled"
        type="number"
        value={value ?? ''}
        onChange={(e) => onChange(name, e.target.value)}
        slotProps={{
            inputLabel: { shrink: true }
        }}
       disabled={disabled}
    />
  )
}
