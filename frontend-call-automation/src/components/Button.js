import React from 'react';
import PropTypes from 'prop-types';

/**
 * Button component for user interactions
 */
const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  type = 'button',
  disabled = false,
  className = '',
  icon = null,
  onClick,
  ...props
}) => {
  const baseClasses = 'btn';
  const variantClasses = `btn-${variant}`;
  const sizeClasses = `btn-${size}`;
  const disabledClasses = disabled ? 'btn-disabled' : '';
  
  const combinedClasses = [
    baseClasses,
    variantClasses,
    sizeClasses,
    disabledClasses,
    className
  ].filter(Boolean).join(' ');

  return (
    <button
      type={type}
      className={combinedClasses}
      disabled={disabled}
      onClick={onClick}
      {...props}
    >
      {icon && <span className="btn-icon">{icon}</span>}
      {children}
    </button>
  );
};

Button.propTypes = {
  /**
   * Button contents
   */
  children: PropTypes.node.isRequired,
  /**
   * Button variant
   */
  variant: PropTypes.oneOf(['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark', 'link']),
  /**
   * Button size
   */
  size: PropTypes.oneOf(['sm', 'md', 'lg']),
  /**
   * Button type
   */
  type: PropTypes.oneOf(['button', 'submit', 'reset']),
  /**
   * Whether the button is disabled
   */
  disabled: PropTypes.bool,
  /**
   * Additional classes
   */
  className: PropTypes.string,
  /**
   * Optional icon
   */
  icon: PropTypes.node,
  /**
   * Click handler
   */
  onClick: PropTypes.func,
};

export default Button;
