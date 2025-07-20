import { Route, Routes, Navigate } from 'react-router-dom'

import Issues from "../pages/Issues";
import Books from "../pages/Books";
import Interviews from "../pages/Interviews";
import AddIssue from '../pages/AddIssue';

function RouteConfig() {
  return (
    <Routes>
      <Route path='/issues' element={<Issues></Issues>}></Route>
      <Route path='/books' element={<Books />}></Route>
      <Route path='/interviews' element={<Interviews />}></Route>
      <Route path='/addIssue' element={< AddIssue/>}></Route>
      <Route path='/' element={<Navigate replace to="/issues"></Navigate>}></Route>
    </Routes>
  )
}

export default RouteConfig;