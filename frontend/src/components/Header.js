import React from 'react';

const Header = () => {
  return (
    <header style={styles.header}>
      <img 
        src="/images/logo.webp" 
        alt="Logo"
        style={styles.logo} 
      />
      <h1 style={styles.title}>Transcription System</h1>
    </header>
  );
};

const styles = {
  header: {
    display: 'flex',
    alignItems: 'center',
    padding: '10px 20px',
    backgroundColor: '#f8f8f8',
    borderBottom: '1px solid #ddd',
  },
  logo: {
    width: '50px',  // Adjust the size as needed
    height: 'auto',
    marginRight: '15px',
  },
  title: {
    fontSize: '24px',
    color: '#333',
  },
};

export default Header;
