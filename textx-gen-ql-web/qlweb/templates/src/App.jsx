import Questionnaire from './pages/questionnaire'
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

function App() {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Questionnaire />
    </LocalizationProvider>
  )
}

export default App
