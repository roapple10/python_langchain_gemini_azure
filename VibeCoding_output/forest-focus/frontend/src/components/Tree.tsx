interface TreeProps {
  stage: 1 | 2 | 3 | 4 | 5
  isKilled?: boolean
  size?: 'small' | 'medium' | 'large'
}

const STAGE_NAMES = {
  1: 'seed',
  2: 'sprout',
  3: 'sapling',
  4: 'young tree',
  5: 'mature tree',
}

export function Tree({ stage, isKilled = false, size = 'medium' }: TreeProps) {
  const stageName = STAGE_NAMES[stage]
  const killedClass = isKilled ? 'tree-killed' : ''

  return (
    <div
      className={`tree tree-stage-${stage} tree-${size} ${killedClass}`}
      role="img"
      aria-label={`Tree stage ${stage}: ${stageName}`}
    >
      <div className="tree-visual">
        {/* Tree visualization will be rendered via CSS */}
      </div>
    </div>
  )
}

