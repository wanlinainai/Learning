import { MyContext1, MyContext2 } from './context';
import ChildCom1 from './components/ChildCom1';


function App(props) {

    return (
        <MyContext1.Provider value={{ a: 1, b: 2, c: 3 }}>
            <MyContext2.Provider value={{ a: 100, b: 200, c: 300 }}>
                <div>
                    <ChildCom1 />
                </div>
            </MyContext2.Provider>
        </MyContext1.Provider>
    );
}

export default App;