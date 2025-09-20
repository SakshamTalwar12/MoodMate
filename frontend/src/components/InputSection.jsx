import React, { useState } from 'react';
import '../styles/InputSection.css';
import TextInput from './TextInput';
import ImageInput from './ImageInput';

const InputSection = ({ 
  activeTab,
  onTextAnalysis, 
  onImageAnalysis, 
  loading 
}) => {
  const renderActiveComponent = () => {
    switch (activeTab) {
      case 'text':
        return <TextInput onAnalysis={onTextAnalysis} loading={loading} />;
      case 'image':
        return <ImageInput onAnalysis={onImageAnalysis} loading={loading} />;
      default:
        return <TextInput onAnalysis={onTextAnalysis} loading={loading} />;
    }
  };

  return (
    <section className="input-section">
      <div className="input-container">
        <div className="tab-content">
          {renderActiveComponent()}
        </div>
      </div>
    </section>
  );
};

export default InputSection;

