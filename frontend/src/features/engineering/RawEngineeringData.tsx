interface RawEngineeringDataProps {
  data: unknown;
}

export default function RawEngineeringData({ data }: RawEngineeringDataProps) {
  return (
    <section className="panel">
      <details>
        <summary>Advanced / Raw Engineering Data</summary>
        <pre className="raw-data">{JSON.stringify(data ?? { status: 'No engineering result yet.' }, null, 2)}</pre>
      </details>
    </section>
  );
}
