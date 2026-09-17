import { useState } from 'react';
import JobDescriptionInput from './components/JobDescriptionInput';
import ResumeUploader from './components/ResumeUploader';
import CandidateResults from './components/CandidateResults';
import { analyzeCandidates } from './services/analysisApi';
import Card from './components/ui/Card';
import Button from './components/ui/Button';

function App() {
  const [jobDescription, setJobDescription] = useState('');
  const [files, setFiles] = useState([]);
  const [topN, setTopN] = useState(2);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const [jobDescriptionError, setJobDescriptionError] = useState('');
  const [filesError, setFilesError] = useState('');

  const validateForm = () => {
    let isValid = true;
    
    if (!jobDescription.trim()) {
      setJobDescriptionError('Job description is required');
      isValid = false;
    } else {
      setJobDescriptionError('');
    }

    if (files.length === 0) {
      setFilesError('At least one resume file is required');
      isValid = false;
    } else {
      setFilesError('');
    }

    if (topN > files.length) {
      setError(`Top N (${topN}) cannot exceed number of uploaded files (${files.length})`);
      isValid = false;
    }

    return isValid;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      const response = await analyzeCandidates(jobDescription, topN, files);
      setResults(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setJobDescription('');
    setFiles([]);
    setTopN(2);
    setResults(null);
    setError(null);
    setJobDescriptionError('');
    setFilesError('');
  };

  const incrementTopN = () => {
    if (topN < files.length) {
      setTopN(topN + 1);
    }
  };

  const decrementTopN = () => {
    if (topN > 1) {
      setTopN(topN - 1);
    }
  };

  return (
    <div className="min-h-screen bg-[#FFF8D9]">
      {/* Header */}
      <header className="border-b border-[#e0e0e0] bg-white">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-lg font-semibold text-[#2d2d2d] tracking-tight">Matchboard</h1>
            </div>
            {results && (
              <button
                onClick={handleReset}
                className="text-sm text-[#666666] hover:text-[#2d2d2d] transition-colors px-3 py-1.5 rounded-lg hover:bg-[#FFF8D9]"
              >
                New analysis
              </button>
            )}
            <div className="text-sm text-[#666666]">AI Candidate Intelligence</div>

          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-6 py-12">
        {!results ? (
          <>
            {/* Hero Section */}
            <div className="mb-8">
              <p className="text-xs font-medium text-[#999999] uppercase tracking-widest mb-2">AI Candidate Intelligence</p>
              <h2 className="text-3xl font-semibold text-[#2d2d2d] mb-3 leading-tight max-w-2xl">
                Find the candidates who fit the role.
              </h2>
              <p className="text-base text-[#666666] leading-relaxed max-w-xl">
                Analyze resumes against your job requirements and identify the strongest candidate matches.
              </p>
            </div>

            {/* Analysis Cards Grid */}
            <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-6">
              {/* Job Description Card */}
              <Card title="Job Description" subtitle="Add the role and requirements you're hiring for" className="min-w-0">
                <JobDescriptionInput
                  value={jobDescription}
                  onChange={setJobDescription}
                  error={jobDescriptionError}
                  compact
                />
              </Card>

              {/* Resume Upload Card */}
              <Card title="Upload Resumes" subtitle="Add multiple PDF or DOCX resumes for analysis" className="min-w-0">
                <ResumeUploader
                  files={files}
                  onFilesChange={setFiles}
                  error={filesError}
                  compact
                />
              </Card>

              {/* Top N Card */}
              <Card title="Select Candidates" subtitle="Choose how many top matches you want to see" className="min-w-0">
                <div className="flex-1">
                  <div className="flex items-center justify-center gap-3 mb-3">
                    <button
                      type="button"
                      onClick={decrementTopN}
                      disabled={topN <= 1}
                      className="w-8 h-8 flex items-center justify-center rounded-lg border border-[#e0e0e0] text-[#666666] hover:border-[#FF9B4A] hover:text-[#FF9B4A] disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                    >
                      −
                    </button>
                    <span className="text-2xl font-medium text-[#2d2d2d] w-10 text-center">
                      {topN}
                    </span>
                    <button
                      type="button"
                      onClick={incrementTopN}
                      disabled={topN >= files.length}
                      className="w-8 h-8 flex items-center justify-center rounded-lg border border-[#e0e0e0] text-[#666666] hover:border-[#FF9B4A] hover:text-[#FF9B4A] disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                    >
                      +
                    </button>
                  </div>
                  <p className="text-xs text-[#999999] text-center">
                    of {files.length || 0} candidates
                  </p>
                </div>
              </Card>

              {/* Analyze Button - Full width row */}
              <div className="md:col-span-3 flex justify-center">
                <Button
                  type="submit"
                  disabled={loading}
                  loading={loading}
                  size="lg"
                  icon={<svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>}
                >
                  {loading ? 'Analyzing candidates...' : 'Analyze candidates'}
                </Button>
              </div>
            </form>

            {/* Error Display */}
            {error && (
              <div className="mb-6 bg-[#FFF8D9] border border-[#FF9B4A] rounded-lg p-4">
                <p className="text-sm text-[#FF9B4A]">{error}</p>
              </div>
            )}
          </>
        ) : (
          <CandidateResults
            results={results.results}
            totalCandidates={results.total_candidates}
            successfulCandidates={results.successful_candidates}
            failedCandidates={results.failed_candidates}
            topN={results.top_n}
            onNewAnalysis={handleReset}
          />
        )}
      </div>
    </div>
  );
}

export default App;
