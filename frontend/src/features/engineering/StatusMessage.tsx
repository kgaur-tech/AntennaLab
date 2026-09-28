import type { EngineeringMessage } from '../../types';

interface StatusMessageProps {
  message: EngineeringMessage;
}

export default function StatusMessage({ message }: StatusMessageProps) {
  return (
    <div className={`status status-${message.level.toLowerCase()}`} role={message.level === 'ERROR' ? 'alert' : 'status'}>
      <strong>{message.title}</strong>
      <span>{message.message}</span>
      {message.field && <small>Field: {message.field}</small>}
    </div>
  );
}
