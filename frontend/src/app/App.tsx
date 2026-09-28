import { useEffect, useState } from 'react';

import EngineeringWorkspace from '../features/engineering/EngineeringWorkspace';
import { ProductPage, ProductShell, type AppRoute, resolveRoute } from '../features/product/ProductPages';
import './styles.css';

export default function App() {
  const [route, setRoute] = useState<AppRoute>(() => resolveRoute(window.location.hash));

  useEffect(() => {
    const onHashChange = () => setRoute(resolveRoute(window.location.hash));
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  const content = route.page === 'workspace' ? <EngineeringWorkspace /> : <ProductPage route={route} />;
  return <ProductShell route={route}>{content}</ProductShell>;
}
