import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Pagination } from '../Pagination';

describe('Pagination', () => {
  it('renders correct page info and disables prev button on first page', () => {
    const handlePageChange = jest.fn();
    render(
      <Pagination
        currentPage={1}
        totalCount={50}
        pageSize={10}
        onPageChange={handlePageChange}
      />
    );

    expect(screen.getByText(/Page/i)).toHaveTextContent('Page 1 of 5');
    expect(screen.getByRole('button', { name: /previous/i })).toBeDisabled();
    expect(screen.getByRole('button', { name: /next/i })).not.toBeDisabled();
  });

  it('calls onPageChange when Next is clicked', () => {
    const handlePageChange = jest.fn();
    render(
      <Pagination
        currentPage={1}
        totalCount={50}
        pageSize={10}
        onPageChange={handlePageChange}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /next/i }));
    expect(handlePageChange).toHaveBeenCalledWith(2);
  });

  it('does not render when totalCount is zero', () => {
    const { container } = render(
      <Pagination
        currentPage={1}
        totalCount={0}
        pageSize={10}
        onPageChange={jest.fn()}
      />
    );
    expect(container.firstChild).toBeNull();
  });
});

