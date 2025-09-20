import React from 'react';
import '../styles/Header.css';

const Header = ({ activeTab, onChangeTab }) => {
  const handleNavClick = (e, tab) => {
    e.preventDefault();
    if (onChangeTab) {
      onChangeTab(tab);
    }
    const target = document.querySelector('.input-section');
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };
  return (
    <header className="header">
      <div className="header-container">
        <div className="logo">
          <h1>🎭 EmotionAI</h1>
          <span className="tagline">Movie Recommendations</span>
        </div>
        
        <nav className="nav">
          <ul className="nav-list">
            <li className="nav-item">
              <a href="#text" className={`nav-link ${activeTab === 'text' ? 'active' : ''}`} onClick={(e) => handleNavClick(e, 'text')}>Text</a>
            </li>
            <li className="nav-item">
              <a href="#image" className={`nav-link ${activeTab === 'image' ? 'active' : ''}`} onClick={(e) => handleNavClick(e, 'image')}>Image</a>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;








