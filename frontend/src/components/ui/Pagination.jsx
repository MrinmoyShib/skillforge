import React from 'react';

export function Pagination({
  currentPage = 1,
  totalCount = 0,
  pageSize = 20,
  onPageChange,
  className = '',
}) {
  const totalPages = Math.ceil(totalCount / pageSize) || 1;
  if (totalPages <= 1) return null;

  const startItem = (currentPage - 1) * pageSize + 1;
  const endItem = Math.min(currentPage * pageSize, totalCount);

  return (
    <div className={`flex flex-col sm:flex-row items-center justify-between gap-4 px-6 py-4 bg-slate-900/60 border-t border-slate-800 text-xs text-slate-400 ${className}`}>
      <div>
        Showing <span className="font-semibold text-white">{startItem}</span> to{' '}
        <span className="font-semibold text-white">{endItem}</span> of{' '}
        <span className="font-semibold text-white">{totalCount}</span> results
      </div>
      <div className="flex items-center gap-2">
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage <= 1}
          className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 disabled:opacity-40 disabled:cursor-not-allowed transition font-medium"
        >
          Previous
        </button>
        <span className="px-3 py-1.5 font-mono text-slate-300">
          Page {currentPage} of {totalPages}
        </span>
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage >= totalPages}
          className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 disabled:opacity-40 disabled:cursor-not-allowed transition font-medium"
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default Pagination;

