import React from 'react';
import CandidateCard from './CandidateCard';
import EmptyState from './ui/EmptyState';

const CandidateResults = ({ results, totalCandidates, successfulCandidates, failedCandidates, topN, onNewAnalysis }) => {
  if (!results || results.length === 0) {
    return (
      <EmptyState
        title="No results to display"
        description="Your ranked candidate results will appear here after analysis."
      />
    );
  }

  const successfulResults = results.filter((r) => r.status === 'success');
  const failedResults = results.filter((r) => r.status === 'failed');

  return (
    <div>
      {/* Results Header */}
      <div className="mb-8">
        <p className="text-xs font-medium text-[#999999] uppercase tracking-widest mb-2">Candidate Intelligence</p>
        <h2 className="text-3xl font-semibold text-[#2d2d2d] mb-3 leading-tight">
          Candidate matches
        </h2>
        <p className="text-base text-[#666666]">
          {totalCandidates} candidate{totalCandidates !== 1 ? 's' : ''} analyzed
        </p>
      </div>

      {/* Summary Stats */}
      <div className="flex gap-6 mb-8 pb-6 border-b border-[#e0e0e0]">
        <div>
          <span className="text-xs text-[#999999] uppercase tracking-wider">Total</span>
          <p className="text-2xl font-semibold text-[#2d2d2d]">{totalCandidates}</p>
        </div>
        <div className="ml-2">
          <span className="text-xs text-[#999999] uppercase tracking-wider">Successful</span>
          <p className="text-2xl font-semibold text-[#50D878]">{successfulCandidates}</p>
        </div>
        {failedCandidates > 0 && (
          <div>
            <span className="text-xs text-[#999999] uppercase tracking-wider">Issues</span>
            <p className="text-2xl font-semibold text-[#FF9B4A]">{failedCandidates}</p>
          </div>
        )}
      </div>

      {/* Top Candidates Section */}
      {successfulResults.length > 0 && (
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-medium text-[#2d2d2d]">Top candidates</h3>
            <span className="text-xs text-[#999999]">Showing top {topN} of {successfulCandidates}</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {successfulResults.map((result, index) => (
              <CandidateCard key={index} result={result} />
            ))}
          </div>
        </div>
      )}

      {/* Failed Resumes Section */}
      {failedResults.length > 0 && (
        <div className="mb-8">
          <details className="group">
            <summary className="flex items-center justify-between cursor-pointer mb-4">
              <h3 className="text-base font-medium text-[#FF9B4A]">
                {failedResults.length} resume{failedResults.length !== 1 ? 's' : ''} couldn't be analyzed
              </h3>
              <svg className="h-4 w-4 text-[#999999] group-open:rotate-180 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </summary>
            <div className="space-y-3">
              {failedResults.map((result, index) => (
                <CandidateCard key={index} result={result} />
              ))}
            </div>
          </details>
        </div>
      )}

      {/* No Successful Candidates */}
      {successfulResults.length === 0 && failedResults.length > 0 && (
        <div className="text-center py-8 bg-[#FFF8D9] border border-[#FF9B4A] rounded-lg">
          <p className="text-[#FF9B4A] font-medium mb-1">No candidates were successfully processed</p>
          <p className="text-[#FF9B4A] text-sm">All resumes encountered processing errors. Please check the files and try again.</p>
        </div>
      )}

      {/* New Analysis Button */}
      {onNewAnalysis && (
        <div className="mt-8 pt-6 border-t border-[#e0e0e0]">
          <button
            onClick={onNewAnalysis}
            className="text-xs text-[#666666] hover:text-[#2d2d2d] transition-colors flex items-center gap-2"
          >
            Start new analysis
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </button>
        </div>
      )}
    </div>
  );
};

export default CandidateResults;
