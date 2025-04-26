/**
 * Module for [brief description of module purpose].
 * 
 * This module provides [detailed description of module functionality and purpose].
 * 
 * @example
 * ```tsx
 * import { SomeComponent } from './components/SomeComponent';
 * 
 * function App() {
 *   return <SomeComponent prop1="value" />;
 * }
 * ```
 */

import { ReactNode } from 'react';

/**
 * Interface for component props
 */
interface SampleComponentProps {
  /** Description of prop1 */
  prop1: string;
  /** Description of prop2, optional */
  prop2?: number;
  /** Description of children */
  children?: ReactNode;
}

/**
 * Sample component description
 * 
 * Longer description with more details about what this component does,
 * its purpose, and any important implementation details.
 * 
 * @component
 * @example
 * ```tsx
 * <SampleComponent prop1="value" prop2={42}>
 *   <div>Child content</div>
 * </SampleComponent>
 * ```
 */
export function SampleComponent({ 
  prop1, 
  prop2 = 0, 
  children 
}: SampleComponentProps): JSX.Element {
  // Component implementation
  return (
    <div>
      {prop1} - {prop2}
      {children}
    </div>
  );
}

/**
 * Sample utility function
 * 
 * Longer description with more details about what this function does,
 * its purpose, and any important implementation details.
 * 
 * @param {string} param1 - Description of param1
 * @param {number[]} param2 - Description of param2
 * @returns {boolean} Description of return value
 * @throws {Error} When param1 is empty
 * 
 * @example
 * ```ts
 * const result = utilityFunction('test', [1, 2, 3]);
 * ```
 */
export function utilityFunction(param1: string, param2: number[]): boolean {
  // Function implementation
  return true;
}

/**
 * Sample type definition
 */
export type SampleType = {
  /** Description of id */
  id: string;
  /** Description of name */
  name: string;
  /** Description of value */
  value: number;
};
