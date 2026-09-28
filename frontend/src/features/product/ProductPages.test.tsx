import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { ProductPage, resolveRoute } from './ProductPages';

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

    expect(screen.getByRole('heading', { name: /from requirements to antenna design/i })).toBeInTheDocument();
    expect(screen.getByText(/internal models and carries its assumptions/i)).toBeInTheDocument();
  });

  it('does not present unavailable Yagi-Uda analysis as calculated', () => {
    render(<ProductPage route={{ page: 'detail', slug: 'yagi-uda' }} />);

    expect(screen.getByText(/No gain, impedance, VSWR, or radiation-pattern values are generated/i)).toBeInTheDocument();
  });
});
