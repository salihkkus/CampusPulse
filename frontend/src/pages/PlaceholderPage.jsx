import React from 'react';

export default function PlaceholderPage({ title, description }) {
  return (
    <section className="glass-card p-8">
      <h2 className="font-h2 text-h2 text-on-surface">{title}</h2>
      <p className="mt-2 max-w-2xl text-body-md text-body-md text-on-surface-variant">{description}</p>
    </section>
  );
}
