import './Input.css';

export default function Input({ label, ...props }) {
  return (
    <div className="hig-input-group">
      {label && <label className="hig-label">{label}</label>}
      <input className="hig-input" {...props} />
    </div>
  );
}
