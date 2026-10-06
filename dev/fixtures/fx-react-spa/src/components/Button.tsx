// Boton base de la UI.
// Trampa del ecosistema #6: forwardRef + memo combinados.
// El orden aqui es `forwardRef(memo(Inner))` (memo adentro, forwardRef afuera).
// CartItem.tsx usa el orden inverso (memo afuera, forwardRef adentro) para
// que la skill note la asimetría.

import { forwardRef, memo } from "react";
import type { ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger";
}

function InnerButton({ variant = "primary", children, ...rest }: ButtonProps) {
  const className = `btn btn-${variant}`;
  return (
    <button className={className} {...rest} data-testid="button">
      {children}
    </button>
  );
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  function Button(props, ref) {
    return <InnerButton {...props} ref={ref} />;
  },
);

Button.displayName = "FxButton";

export const MemoizedButton = memo(Button);