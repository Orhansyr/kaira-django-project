'use client';

import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchComponentBySlug } from '@/lib/redux/slices/pageComponentSlice';

const PageComponentViewer = ({ slug }) => {
  const dispatch = useDispatch();
  // Select the specific component, and the overall status/error for the slice
  const component = useSelector((state) => state.pageComponents.components[slug]);
  const { status, error } = useSelector((state) => state.pageComponents);

  useEffect(() => {
    // Only fetch if the component for this slug is not already loaded or loading
    if (!component) {
      dispatch(fetchComponentBySlug(slug));
    }
  }, [slug, component, dispatch]);

  if (status === 'loading' && !component) {
    return <div className="p-8">Loading component...</div>;
  }

  if (error && !component) {
    // Show error only if this specific component failed to load
    return <div className="p-8 text-red-500">Error loading component: {error.detail || 'Not found'}</div>;
  }

  if (!component) {
    // This can be shown if the component is not found after a successful fetch,
    // or if the initial state is rendered before loading starts.
    return <div className="p-8">Component '{slug}' not found.</div>;
  }

  return (
    <div className="p-8 bg-white shadow-md rounded-lg">
      <h1 className="text-3xl font-bold mb-4">{component.title}</h1>
      {/* The content from the admin can be trusted, but in a real-world scenario,
          you would want to sanitize this HTML to prevent XSS attacks. */}
      <div dangerouslySetInnerHTML={{ __html: component.content }} />
    </div>
  );
};

export default PageComponentViewer;
