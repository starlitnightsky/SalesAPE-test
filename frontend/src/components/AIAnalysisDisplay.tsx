import React from 'react';
import { AIAnalysis } from '../types/joke';

interface AIAnalysisDisplayProps {
  analysis: AIAnalysis;
  contextResponse?: string;
}

export const AIAnalysisDisplay: React.FC<AIAnalysisDisplayProps> = ({ analysis, contextResponse }) => {
  return (
    <div className="ai-analysis">
      <div className="ai-analysis-header">
        <h3>🤖 AI Analysis</h3>
        <div className="ai-badge">Powered by LLM</div>
      </div>
      
      {contextResponse && (
        <div className="context-response">
          <p>{contextResponse}</p>
        </div>
      )}
      
      <div className="analysis-details">
        <div className="analysis-item">
          <strong>Category:</strong> {analysis.category}
        </div>
        
        <div className="analysis-item">
          <strong>User Mood:</strong> {analysis.user_mood}
        </div>
        
        {analysis.keywords.length > 0 && (
          <div className="analysis-item">
            <strong>Keywords:</strong>
            <div className="keywords">
              {analysis.keywords.map((keyword, index) => (
                <span key={index} className="keyword-tag">{keyword}</span>
              ))}
            </div>
          </div>
        )}
        
        <div className="analysis-item">
          <strong>AI Reasoning:</strong>
          <p className="reasoning">{analysis.reasoning}</p>
        </div>
        
        <div className="analysis-item">
          <strong>Suggested Amount:</strong> {analysis.suggested_amount} jokes
        </div>
      </div>
    </div>
  );
}; 