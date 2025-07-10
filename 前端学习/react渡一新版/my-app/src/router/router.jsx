import React from 'react';
import { useRoutes, Navigate } from 'react-router-dom';
import Home from '../components/Home';
import AddOrEdit from '../components/AddOrEdit';
import Detail from '../components/Detail';
import About from '../components/About';
import Tel from '../components/Tel';
import Email from '../components/Email';

function Router() {
  const routerConfig = useRoutes([
    {
      path: '/home',
      element: <Home />
    }, {
      path: "/about",
      element: <About />,
      children: [
        {
          path: "email",
          element: <Email />
        }, {
          path: "tel",
          element: <Tel />
        }, {
          path: "",
          element: <Navigate replace to="email"></Navigate>
        }
      ]
    }, {
      path: '/add',
      element: <AddOrEdit />
    }, {
      path: "/detail/:id",
      element: <Detail />
    }, {
      path: '/edit/:id',
      element: <AddOrEdit />
    }, {
      path: '/',
      element: <Navigate replace to="/home" />
    }
  ])

  return routerConfig;
}

export default Router;