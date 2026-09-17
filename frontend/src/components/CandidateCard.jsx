import React, { useState } from 'react';
import Card from './ui/Card';

const CandidateCard = ({ result }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (result.status === 'failed') {
    return (
      <div className="px-4 py-3 bg-[#FFF8D9] border border-[#FF9B4A] rounded-lg">
        <div className="flex items-center mb-1">
          <svg className="h-4 w-4 text-[#FF9B4A] mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="text-sm font-medium text-[#FF9B4A]">Processing failed</span>
        </div>
        <p className="text-sm font-medium text-[#2d2d2d]">{result.filename}</p>
        <p className="text-sm text-[#FF9B4A] mt-0.5">{result.error}</p>
      </div>
    );
  }

  const { candidate, match, rank, filename } = result;
  const score = match.score || 0;
  const details = match.details || {};

  const formatRank = (num) => num.toString().padStart(2, '0');

  return (
    <Card className="overflow-hidden">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start gap-3 flex-1">
          {/* Rank */}
          <div className="text-2xl font-semibold text-[#666666] font-mono">
            {formatRank(rank)}
          </div>

          {/* Candidate Info */}
          <div className="flex-1 min-w-0">
            <h3 className="text-base font-medium text-[#2d2d2d] mb-1">
              {candidate.name || 'Unknown Candidate'}
            </h3>
            <p className="text-xs text-[#666666] mb-1">{filename}</p>

            {candidate.total_experience_years !== null && candidate.total_experience_years !== undefined && (
              <p className="text-xs text-[#666666]">
                {candidate.total_experience_years} years experience
              </p>
            )}
          </div>
        </div>

        {/* Score */}
        <div className="text-right ml-3">
          <div className="text-3xl font-semibold text-[#2d2d2d]">{Math.round(score)}</div>
          <div className="text-xs text-[#999999] mt-1">Match score</div>
        </div>
      </div>

      {/* Skills Preview */}
      {candidate.skills && candidate.skills.length > 0 && (
        <div className="mb-4 flex flex-wrap gap-1.5">
          {candidate.skills.slice(0, 6).map((skill, index) => (
            <span
              key={index}
              className="px-2 py-1 bg-[#20C4CF] text-white text-xs rounded-md"
            >
              {skill}
            </span>
          ))}
          {candidate.skills.length > 6 && (
            <span className="text-xs text-[#999999]">
              +{candidate.skills.length - 6} more
            </span>
          )}
        </div>
      )}

      {/* Expand Button */}
      <button
        type="button"
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center gap-2 text-xs text-[#2d2d2d] hover:text-[#666666] font-medium transition-colors"
      >
        {isExpanded ? 'Hide analysis' : 'View analysis'}
        <svg className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Expandable Details */}
      {isExpanded && (
        <div className="mt-4 pt-4 border-t border-[#e0e0e0]">
          {candidate.email && (
            <div className="mb-3">
              <span className="text-xs font-medium text-[#666666] uppercase tracking-wider">Email</span>
              <p className="text-sm text-[#2d2d2d] mt-1">{candidate.email}</p>
            </div>
          )}

          {details && Object.keys(details).length > 0 && (
            <div className="space-y-3">
              {Object.entries(details).map(([key, value]) => (
                <div key={key}>
                  <span className="text-xs font-medium text-[#666666] uppercase tracking-wider">
                    {key.replace(/_/g, ' ')}
                  </span>
                  <div className="text-sm text-[#2d2d2d] mt-1">
                    {Array.isArray(value) ? (
                      <div className="flex flex-wrap gap-1">
                        {value.map((item, idx) => (
                          <span key={idx} className="inline-flex items-center">
                            {key.includes('matching') || key.includes('matched') ? (
                              <span className="text-[#50D878] mr-1">✓</span>
                            ) : key.includes('missing') ? (
                              <span className="text-[#FF9B4A] mr-1">○</span>
                            ) : null}
                            {typeof item === 'string' ? item : String(item)}
                            {idx < value.length - 1 && <span className="text-[#999999] mx-1">•</span>}
                          </span>
                        ))}
                      </div>
                    ) : (
                      String(value)
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </Card>
  );
};

export default CandidateCard;
