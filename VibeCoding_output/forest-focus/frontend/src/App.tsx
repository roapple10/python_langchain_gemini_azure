import { useTimer } from './hooks/useTimer'
import { useUserPreferences } from './hooks/useUserPreferences'
import { Timer } from './components/Timer'
import { Tree } from './components/Tree'
import { DurationPicker } from './components/DurationPicker'
import './styles/global.css'
import './styles/timer.css'
import './styles/tree.css'
import './styles/duration-picker.css'

function App() {
  const { preferences, updateFocusDuration, isLoading } = useUserPreferences()
  const durationSeconds = preferences.focusDurationMinutes * 60

  const handleComplete = () => {
    console.log('Session completed!')
    // TODO: Save to forest (User Story 3)
  }

  const timer = useTimer(durationSeconds, handleComplete)
  const hasActiveSession = timer.isActive && timer.remainingSeconds < durationSeconds

  return (
    <main style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <header style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h1 style={{ fontSize: '2.5rem', color: 'var(--color-primary)', marginBottom: '0.5rem' }}>
          Forest Focus
        </h1>
        <p style={{ color: 'var(--color-text-secondary)' }}>Pomodoro Timer</p>
      </header>

      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '3rem' }}>
        <Tree stage={timer.currentStage as 1 | 2 | 3 | 4 | 5} size="large" />

        {!isLoading && (
          <DurationPicker
            value={preferences.focusDurationMinutes}
            onChange={updateFocusDuration}
            disabled={hasActiveSession}
          />
        )}

        <Timer
          remainingSeconds={timer.remainingSeconds}
          durationSeconds={durationSeconds}
          isPaused={timer.isPaused}
          onStart={timer.start}
          onPause={timer.pause}
          onResume={timer.resume}
          onCancel={timer.cancel}
        />
      </div>
    </main>
  )
}

export default App

