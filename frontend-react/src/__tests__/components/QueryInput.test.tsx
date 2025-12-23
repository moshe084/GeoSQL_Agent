/**
 * QueryInput component tests
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryInput } from '../../components/QueryInput';

describe('QueryInput Component', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders query input form', () => {
    render(<QueryInput onSubmit={mockOnSubmit} />);

    expect(screen.getByLabelText(/ask a question/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /execute query/i })).toBeInTheDocument();
  });

  test('submit button is disabled when question is empty', () => {
    render(<QueryInput onSubmit={mockOnSubmit} />);

    const submitButton = screen.getByRole('button', { name: /execute query/i });
    expect(submitButton).toBeDisabled();
  });

  test('submit button is enabled when question is entered', async () => {
    render(<QueryInput onSubmit={mockOnSubmit} />);

    const textarea = screen.getByLabelText(/ask a question/i);
    const submitButton = screen.getByRole('button', { name: /execute query/i });

    await userEvent.type(textarea, 'Show all cafes');

    expect(submitButton).toBeEnabled();
  });

  test('calls onSubmit with question when form is submitted', async () => {
    render(<QueryInput onSubmit={mockOnSubmit} />);

    const textarea = screen.getByLabelText(/ask a question/i);
    const submitButton = screen.getByRole('button', { name: /execute query/i });

    await userEvent.type(textarea, 'Show all cafes');
    fireEvent.click(submitButton);

    expect(mockOnSubmit).toHaveBeenCalledWith('Show all cafes');
  });

  test('shows loading state when isLoading is true', () => {
    render(<QueryInput onSubmit={mockOnSubmit} isLoading={true} />);

    expect(screen.getByText(/processing/i)).toBeInTheDocument();
    expect(screen.getByRole('button')).toBeDisabled();
  });

  test('renders example queries', () => {
    render(<QueryInput onSubmit={mockOnSubmit} />);

    expect(screen.getByText(/try these examples/i)).toBeInTheDocument();
  });

  test('clicking example query fills the textarea', async () => {
    render(<QueryInput onSubmit={mockOnSubmit} />);

    const exampleButton = screen.getAllByRole('button')[1]; // First example button
    fireEvent.click(exampleButton);

    const textarea = screen.getByLabelText(/ask a question/i) as HTMLTextAreaElement;
    expect(textarea.value).not.toBe('');
  });

  test('trims whitespace from question before submission', async () => {
    render(<QueryInput onSubmit={mockOnSubmit} />);

    const textarea = screen.getByLabelText(/ask a question/i);
    const submitButton = screen.getByRole('button', { name: /execute query/i });

    await userEvent.type(textarea, '  Show all cafes  ');
    fireEvent.click(submitButton);

    expect(mockOnSubmit).toHaveBeenCalledWith('Show all cafes');
  });

  test('does not submit when disabled', async () => {
    render(<QueryInput onSubmit={mockOnSubmit} disabled={true} />);

    const textarea = screen.getByLabelText(/ask a question/i);
    const submitButton = screen.getByRole('button', { name: /execute query/i });

    await userEvent.type(textarea, 'Show all cafes');
    fireEvent.click(submitButton);

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});
