import * as React from 'react';
import { cn } from '@/lib/utils';
import { Label } from './Label';

interface FormProps extends React.FormHTMLAttributes<HTMLFormElement> {}

const Form = React.forwardRef<HTMLFormElement, FormProps>(({ className, ...props }, ref) => (
  <form ref={ref} className={cn('space-y-6', className)} {...props} />
));
Form.displayName = 'Form';

interface FormFieldProps {
  children: React.ReactNode;
  className?: string;
}

const FormField = React.forwardRef<HTMLDivElement, FormFieldProps>(({ className, children }, ref) => (
  <div ref={ref} className={cn('space-y-2', className)}>
    {children}
  </div>
));
FormField.displayName = 'FormField';

interface FormLabelProps extends React.ComponentPropsWithoutRef<typeof Label> {
  required?: boolean;
}

const FormLabel = React.forwardRef<HTMLLabelElement, FormLabelProps>(
  ({ className, required, children, ...props }, ref) => (
    <Label ref={ref} className={cn(className)} {...props}>
      {children}
      {required && <span className="ml-1 text-destructive">*</span>}
    </Label>
  )
);
FormLabel.displayName = 'FormLabel';

interface FormMessageProps extends React.HTMLAttributes<HTMLParagraphElement> {
  error?: boolean;
}

const FormMessage = React.forwardRef<HTMLParagraphElement, FormMessageProps>(
  ({ className, error, children, ...props }, ref) => {
    if (!children) return null;

    return (
      <p
        ref={ref}
        className={cn('text-sm', error ? 'text-destructive' : 'text-muted-foreground', className)}
        {...props}
      >
        {children}
      </p>
    );
  }
);
FormMessage.displayName = 'FormMessage';

interface FormDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {}

const FormDescription = React.forwardRef<HTMLParagraphElement, FormDescriptionProps>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn('text-sm text-muted-foreground', className)} {...props} />
  )
);
FormDescription.displayName = 'FormDescription';

export { Form, FormField, FormLabel, FormMessage, FormDescription };
