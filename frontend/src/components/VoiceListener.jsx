import { useState, useEffect, useRef, useCallback } from 'react';

const WAKE_PHRASES = ['doxa', 'show chat', 'hey doxa', 'open chat'];
const DISMISS_PHRASES = ['hide chat', 'close chat', 'dismiss'];

function matchesPhrase(transcript, phrases) {
  const lower = transcript.toLowerCase().trim();
  return phrases.some(
    (phrase) => lower.includes(phrase)
  );
}

export default function VoiceListener({ onActivate, onDeactivate }) {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);
  const shouldListenRef = useRef(true);
  const restartTimeoutRef = useRef(null);

  const SpeechRecognition =
    typeof window !== 'undefined'
      ? window.SpeechRecognition || window.webkitSpeechRecognition
      : null;

  const startListening = useCallback(() => {
    if (!SpeechRecognition || !shouldListenRef.current) return;

    try {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }

        if (matchesPhrase(transcript, WAKE_PHRASES)) {
          onActivate?.();
        } else if (matchesPhrase(transcript, DISMISS_PHRASES)) {
          onDeactivate?.();
        }
      };

      recognition.onerror = (event) => {
        // 'no-speech' and 'aborted' are expected during continuous listening
        if (event.error !== 'no-speech' && event.error !== 'aborted') {
          console.warn('[VoiceListener] Recognition error:', event.error);
        }
      };

      recognition.onend = () => {
        setIsListening(false);
        // Auto-restart after a short delay (browser periodically stops recognition)
        if (shouldListenRef.current) {
          restartTimeoutRef.current = setTimeout(() => {
            startListening();
          }, 300);
        }
      };

      recognitionRef.current = recognition;
      recognition.start();
    } catch (err) {
      console.warn('[VoiceListener] Could not start recognition:', err);
      setIsListening(false);
    }
  }, [SpeechRecognition, onActivate, onDeactivate]);

  useEffect(() => {
    shouldListenRef.current = true;
    startListening();

    return () => {
      shouldListenRef.current = false;
      if (restartTimeoutRef.current) {
        clearTimeout(restartTimeoutRef.current);
      }
      if (recognitionRef.current) {
        try {
          recognitionRef.current.abort();
        } catch {
          // ignore
        }
        recognitionRef.current = null;
      }
    };
  }, [startListening]);

  // If API is unavailable, render nothing
  if (!SpeechRecognition) return null;

  return (
    <div
      className={isListening ? 'voice-dot' : 'voice-dot-off'}
      title={isListening ? 'Voice listener active' : 'Voice listener inactive'}
      style={{
        position: 'fixed',
        top: '16px',
        right: '16px',
        zIndex: 50,
        width: '8px',
        height: '8px',
        borderRadius: '50%',
        backgroundColor: isListening ? '#dc143c' : '#2a3444',
        boxShadow: isListening
          ? '0 0 8px rgba(220, 20, 60, 0.6), 0 0 20px rgba(220, 20, 60, 0.2)'
          : 'none',
        transition: 'all 0.3s ease',
        pointerEvents: 'none',
      }}
    />
  );
}
