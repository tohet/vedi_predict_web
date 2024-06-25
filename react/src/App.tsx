
import React, {useState} from "react"
import axios from "axios"
import './App.css'
import logo from './assets/vedi_logo.png';
import interp from './assets/vedi_interp.png';

interface Article {
  title: string
  authors: string
  topics: string
}

function App() {
    const [_title, setTitle] = useState('')
    const [_authors, setAuthors] = useState('')
    const [_topics, setTopics] = useState('')
    const [_pred, setPred] = useState(0)
    const [_label, setLabel] = useState('???')
    
// a function to givwe title, authors and topics to the model
    const predict_views = async () => {
      const articleSubmission: Article = {
        title: _title,
        authors: _authors,
        topics: _topics
      }
      try {
        let {data} = await axios.post<Article>(
          "http://localhost:8000/api",
          articleSubmission,
          {
            headers: {
              Accept: 'application/json',
            },
          },
        )

        setTitle(articleSubmission.title)
        setAuthors(articleSubmission.authors)
        setTopics(articleSubmission.topics)
        catchPred()
      }
      catch (e) {
        console.debug(e)
        
        return
    }
    }
// a function to get prediction from model
    const catchPred = async () => {
      try{
      let pred_score = await axios.get("http://localhost:8000/api")
      let result = pred_score.data.score
      let res_label = pred_score.data.label
      console.debug("got pred")
      setPred(result)
      setLabel(res_label)
      }
      catch (e) {
        console.debug(e)
          
        return
    }
    }

    return (
      <div>
          <div className="logo">
            <img src={logo} height={250}/>
         </div>

          <h5 className="sub_title">
            Древние тексты скажут, что твоя статья отстой
          </h5>

          <h6 className="instruct">
            Как пользоваться: Введите заголовок статьи (без подзаголовка) в поле "Заголовок", введите автора в поле "Авторы"(если их несколько, напишите через запятую и с заглавных, например: Василий Пупкин, Иван Иванов), напишите рубрики в газете в "Рубрики" (если несколько, то так же, через запятую и с заглавной: Экономика, Политика). Наконец, нажмите "Предсказать", приблизительное число просмторов можно узнать по схеме ниже.
          </h6>

          <div>
            <input type="text" placeholder="Заголовок" value={_title} onChange={e => setTitle(e.target.value)} size={100}/>
          </div>
          
          <input type="text" placeholder="Авторы" value={_authors} onChange={e => setAuthors(e.target.value)} size={38}/>
          <input type="text" placeholder="Рубрики" value={_topics} onChange={e => setTopics(e.target.value)} size={38}/>
          <button onClick={predict_views}>Предсказать</button>

          <div className="num_score">
            Текст набрал {_pred} очков Ведов.
            
          </div>

          <div className="label_score">
            Этот текст: {_label}
          </div>

          <div className="interp">
            <img src={interp} height={200}/>
         </div>

      </div>

      
  )
}
export default App
