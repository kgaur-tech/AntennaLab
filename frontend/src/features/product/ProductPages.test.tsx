import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it } from 'vitest';

import { ProductPage, ProductShell, resolveRoute } from './ProductPages';

afterEach(() => {
  window.localStorage.removeItem('antennaLab.theme');
  delete document.documentElement.dataset.theme;
});

describe('product routing and representative pages', () => {
  it('resolves product routes without a router dependency', () => {
    expect(resolveRoute('#/')).toEqual({ page: 'home' });
    expect(resolveRoute('#/explore/yagi-uda')).toEqual({ page: 'detail', slug: 'yagi-uda' });
    expect(resolveRoute('#/design/example-1')).toEqual({ page: 'workspace' });
    expect(resolveRoute('#/learn/fundamentals')).toEqual({ page: 'learn', slug: 'fundamentals' });
    expect(resolveRoute('#/manufacturing')).toEqual({ page: 'manufacturing' });
  });

  it('communicates the engineering workflow on the home page', () => {
    render(<ProductPage route={{ page: 'home' }} />);

    expect(screen.getByRole('heading', { name: /from requirements\s*to a real antenna/i })).toBeInTheDocument();
    expect(screen.getByText(/Internal, versioned models/i)).toBeInTheDocument();
  });

  it('does not present unavailable Yagi-Uda analysis as calculated', () => {
    render(<ProductPage route={{ page: 'detail', slug: 'yagi-uda' }} />);

    expect(screen.getByText(/No gain, impedance, VSWR, or radiation-pattern values are generated/i)).toBeInTheDocument();
  });

  it('persists an accessible theme choice through the product shell', async () => {
    const user = userEvent.setup();
    render(<ProductShell route={{ page: 'home' }}><div>Product content</div></ProductShell>);

    await user.click(screen.getByRole('button', { name: /switch to dark theme/i }));

    expect(document.documentElement.dataset.theme).toBe('dark');
    expect(window.localStorage.getItem('antennaLab.theme')).toBe('dark');
    expect(screen.getByRole('button', { name: /switch to light theme/i })).toBeInTheDocument();
  });
});
