import React from 'react';
import ReactPlayer from 'react-player';

const MediaPlayer = ({ file }) => {
  return (
    <div className="player-wrapper">
      <ReactPlayer
        url={`http://localhost:9010/api/download/${file}`}
        controls={true}
        width="100%"
        height="100%"
      />
    </div>
  );
};

export default MediaPlayer;
