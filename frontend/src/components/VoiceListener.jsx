import { useState, useEffect, useRef, useCallback } from 'react';

const WAKE_PHRASES = ['hey doxa', 'ok doxa', 'doxa', 'hey dox', 'open sphere', 'show sphere', 'sphere mode'];
const DISMISS_PHRASES = ['doxa stop', 'stop', 'exit', 'close sphere', 'exit sphere', 'go back', 'dismiss'];

function matchesPhrase(transcript, phrases) {
  const lower = transcript.toLowerCase().trim();
  return phrases.some((phrase) => lower.includes(phrase));
}

export default function VoiceListener({ onActivate, onDeactivate, onPermissionError, onQueryCaptured, isSphereMode }) {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);
  const shouldListenRef = useRef(true);
  const restartTimeoutRef = useRef(null);
  const lastTriggerRef = useRef(0);

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

        const now = Date.now();

        // Check dismiss phrases first
        if (matchesPhrase(transcript, DISMISS_PHRASES)) {
          if (now - lastTriggerRef.current > 1500) {
            lastTriggerRef.current = now;
            onDeactivate?.();
          }
          return;
        }

        // Check wake phrases
        if (matchesPhrase(transcript, WAKE_PHRASES)) {
          if (now - lastTriggerRef.current > 1500) {
            lastTriggerRef.current = now;
            onActivate?.();
          }
          return;
        }

        // If currently in sphere mode and user speaks a query (longer than 3 chars), deliver query
        if (isSphereMode && transcript.trim().length > 3 && event.results[event.results.length - 1]?.isFinal) {
          const cleanQuery = transcript
            .replace(/hey doxa|ok doxa|doxa|hey dox/gi, '')
            .trim();
          if (cleanQuery.length > 2) {
            onQueryCaptured?.(cleanQuery);
          }
        }
      };

      recognition.onerror = (event) => {
        if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
          console.warn('[VoiceListener] Microphone permission denied');
          onPermissionError?.();
        } else if (event.error !== 'no-speech' && event.error !== 'aborted') {
          console.warn('[VoiceListener] Recognition error:', event.error);
        }
      };

      recognition.onend = () => {
        setIsListening(false);
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
  }, [SpeechRecognition, onActivate, onDeactivate, onPermissionError, onQueryCaptured, isSphereMode]);

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

  if (!SpeechRecognition) return null;

  return (
    <div
      className={isListening ? 'voice-dot' : 'voice-dot-off'}
      title={isListening ? 'Voice listener active (Say "Hey Doxa")' : 'Voice listener inactive'}
      style={{
        position: 'fixed',
        top: '16px',
        right: '16px',
        zIndex: 50,
        width: '8px',
        height: '8px',
        borderRadius: '50%',
        backgroundColor: isListening ? 'var(--jarvis-accent)' : '#2a3444',
        boxShadow: isListening
          ? '0 0 8px rgba(var(--jarvis-accent-rgb), 0.6), 0 0 20px rgba(var(--jarvis-accent-rgb), 0.2)'
          : 'none',
        transition: 'all 0.3s ease',
        pointerEvents: 'none',
      }}
    />
  );
}
