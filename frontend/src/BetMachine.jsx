import React, { useState } from 'react';
import { ArrowLeft } from 'lucide-react';

const BetMachine = () => {
  const [currentPage, setCurrentPage] = useState('home');
  const [history, setHistory] = useState([]);
  const [selectedProp, setSelectedProp] = useState(null);
  const [playerName, setPlayerName] = useState('');
  const [pitcherName, setPitcherName] = useState('');
  const [formErrors, setFormErrors] = useState({});

  const handlePlayerNameChange = (newValue) => {
    setPlayerName(newValue);
  };

  const handlePitcherNameChange = (newValue) => {
    setPitcherName(newValue);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://localhost:3000/api/submit-names', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          player_name: playerName,
          pitcher_name: pitcherName,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        console.log('Names submitted successfully:', data);
        // Handle successful submission (e.g., navigate to next page)
      } else {
        setFormErrors(data.errors || {});
      }
    } catch (error) {
      console.error('Error submitting names:', error);
    }
  };

  const handlePropSelection = (prop) => {
    setSelectedProp(prop);
    navigateTo('choosePlayerPitcher');
  };

  const navigateTo = (page) => {
    setHistory([...history, currentPage]);
    setCurrentPage(page);
  };

  const goBack = () => {
    if (history.length > 0) {
      const prevPage = history.pop();
      setCurrentPage(prevPage);
      setHistory([...history]);
    }
  };

  const Button = ({ onClick, children }) => (
    <button
      onClick={onClick}
      className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-4 px-6 rounded-lg text-xl m-4 transition duration-300 ease-in-out transform hover:scale-105"
    >
      {children}
    </button>
  );

  const BackButton = () => (
    <button onClick={goBack} className="absolute top-6 left-6 text-white p-2 rounded-full bg-gray-800 hover:bg-gray-700">
      <ArrowLeft size={32} />
    </button>
  );

  const TextInput = ({ label, value, onChange, error }) => (
    <div className="m-4 w-full max-w-xs">
      <label className="block text-xl font-bold mb-2">{label}</label>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-gray-700 text-white py-3 px-4 rounded-lg text-xl"
        placeholder={`Enter ${label.toLowerCase()}'s name`}
      />
      {error && <p className="text-red-500 mt-1">{error}</p>}
    </div>
  );

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return (
          <div className="flex flex-col items-center justify-center h-full">
            <h1 className="text-5xl font-bold mb-12">Ben's Bet Machine</h1>
            <h2 className="text-3xl mb-8">Choose your bet type:</h2>
            <div className="flex flex-wrap justify-center">
              <Button onClick={() => navigateTo('playerProps')}>Player Props</Button>
              <Button onClick={() => navigateTo('gameLines')}>Game Lines</Button>
            </div>
          </div>
        );
      case 'playerProps':
        return (
          <div className="flex flex-col items-center justify-center h-full">
            <BackButton />
            <h2 className="text-4xl mb-8">Choose your Player Prop:</h2>
            <div className="grid grid-cols-2 gap-6">
              <Button onClick={() => handlePropSelection('hits')}>Hits</Button>
              <Button onClick={() => handlePropSelection('rbis')}>RBIs</Button>
              <Button onClick={() => handlePropSelection('pitcherKs')}>Pitcher Ks</Button>
              <Button onClick={() => handlePropSelection('pitcherBBs')}>Pitcher BBs</Button>
            </div>
          </div>
        );

      case 'choosePlayerPitcher':
        return (
          <div className="flex flex-col items-center justify-center h-full">
            <BackButton />
            <h2 className="text-4xl mb-8">Enter Player and Opposing Pitcher:</h2>
            <div className="flex flex-wrap justify-center">
              <TextInput 
                label="Player" 
                value={playerName} 
                onChange={handlePlayerNameChange}
                error={formErrors.player_name}
              />
              <TextInput 
                label="Pitcher" 
                value={pitcherName} 
                onChange={handlePitcherNameChange}
                error={formErrors.pitcher_name}
              />
            </div>
            <button 
              onClick={handleSubmit}
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
            >
              Submit
            </button>
          </div>
        );
      case 'choosePitcherTeam':
        return (
          <div className="flex flex-col items-center justify-center h-full">
            <BackButton />
            <h2 className="text-4xl mb-8">Enter Pitcher and Opposing Team:</h2>
            <div className="flex flex-wrap justify-center">
              <TextInput 
                label="Pitcher" 
                value={pitcherName} 
                onChange={(value) => setPitcherName(value)} 
              />
              <TextInput 
                label="Team" 
                value={playerName} 
                onChange={(value) => setPlayerName(value)} 
              />
            </div>
            <Button onClick={() => console.log(`Pitcher: ${pitcherName}, Team: ${playerName}`)}>Next</Button>
          </div>
        );
      case 'gameLines':
        return (
          <div className="flex flex-col items-center justify-center h-full">
            <BackButton />
            <h2 className="text-4xl mb-8">Choose your Game Line:</h2>
            <div className="grid grid-cols-2 gap-6">
              <Button onClick={() => {}}>Run Line</Button>
              <Button onClick={() => {}}>Moneyline</Button>
              <Button onClick={() => {}}>Team Total Runs</Button>
              <Button onClick={() => {}}>Game Total Runs</Button>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="bg-gray-900 text-white min-h-screen flex items-center justify-center">
      <div className="w-full h-screen p-8">
        {renderPage()}
      </div>
    </div>
  );
};

export default BetMachine;