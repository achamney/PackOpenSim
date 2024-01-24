import { render, screen } from '@testing-library/react';
import App from './App';

test('TODO', () => {
  render(<App />);
  const linkElement = screen.getByText(/TODO/i);
  expect(linkElement).toBeInTheDocument();
});
