import './Button.css';

export default function Button({ children, ...props }) {
  return (
    <button className="hig-button" {...props}>
      {children}
    </button>
  );
}
