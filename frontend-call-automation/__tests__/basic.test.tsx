import { render, screen } from '@testing-library/react';

describe('Basic test', () => {
  it('passes a basic test', () => {
    expect(true).toBe(true);
  });

  it('can render a simple component', () => {
    render(<div data-testid="test-element">Test Component</div>);
    const element = screen.getByTestId('test-element');
    expect(element).toBeInTheDocument();
    expect(element).toHaveTextContent('Test Component');
  });
});
