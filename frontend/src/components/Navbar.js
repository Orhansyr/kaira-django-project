'use client';

import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMenus } from '@/lib/redux/slices/menuSlice';
import Link from 'next/link';

const MenuItem = ({ item }) => {
  return (
    <li className="relative group">
      <Link href={item.url} className="p-4 block hover:bg-gray-700">
        {item.name}
      </Link>
      {item.children && item.children.length > 0 && (
        <ul className="absolute left-0 top-full bg-gray-800 hidden group-hover:block w-48">
          {item.children.map(child => <MenuItem key={child.id} item={child} />)}
        </ul>
      )}
    </li>
  );
};

const Navbar = () => {
  const dispatch = useDispatch();
  const { items: menus, status, error } = useSelector((state) => state.menus);

  useEffect(() => {
    // We fetch menus only if they haven't been fetched yet.
    if (status === 'idle') {
      dispatch(fetchMenus());
    }
  }, [status, dispatch]);

  return (
    <nav className="bg-gray-800 text-white">
      <div className="container mx-auto">
        <ul className="flex items-center">
          {status === 'loading' && <li className="p-4">Loading...</li>}
          {status === 'succeeded' && menus.map(item => <MenuItem key={item.id} item={item} />)}
          {status === 'failed' && <li className="p-4 text-red-500">Error: {error}</li>}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
