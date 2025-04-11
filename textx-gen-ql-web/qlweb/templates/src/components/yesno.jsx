export default function YesNoField({ name, label, value, onChange, disabled = false}) {
  return (
    <div>
      <p>{label}</p>
      <label style={{paddingRight: '20px'}}>
        <input
          type="radio"
          name={name}
          checked={value === undefined}
          onChange={(_) => {
            onChange(name, undefined)
          }}
          disabled={disabled}
        />
        Unanswered
      </label>

      <label style={{paddingRight: '20px'}}>
        <input
          type="radio"
          name={name}
          checked={value === 'true'}
          onChange={(_) => {
            onChange(name, 'true')
          }}
          disabled={disabled}
        />
        Yes
      </label>

      <label>
        <input
          type="radio"
          name={name}
          checked={value === 'false'}
          onChange={(_) => {
            onChange(name, 'false')
          }}
          disabled={disabled}
        />
        No
      </label>
    </div>
  );
}
