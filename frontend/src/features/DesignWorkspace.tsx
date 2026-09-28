interface DesignWorkspaceProps {
  family: string;
  frequencyHz: number;
}

export default function DesignWorkspace({ family, frequencyHz }: DesignWorkspaceProps) {
  return (
    <section>
      <h3>Design Workspace</h3>
      <p>Selected family: {family}</p>
      <p>Frequency: {frequencyHz} Hz</p>
      <p>Geometry and simulation controls will be implemented in the next engineering phase.</p>
    </section>
  );
}
