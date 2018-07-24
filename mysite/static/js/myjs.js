window.onload=function(){
    var pos=0,total=0,question,a,b,c,d,ques,correct=0,choice;
    {% for q in question%}
      total=total+1;
    {% endfor %}

    function _(x){
      return document.getElementById(x);
    }
    var x;

      ques="{{question.0|safe}}";
      a="{{question.1|safe}}";
      b="{{question.2|safe}}";
      c="{{question.3|safe}}";
      d="{{question.4|safe}}";
    function renderQuestion(){
      if(pos>=1){
        test.innerHTML="<h2>Points you got :" +correct+"</h2>";
      }
      test=_("test");
      _("test_status").innerHTML="Question "+(pos+1)+" of "+total;
      test.innerHTML="<h3>"+ques+"</h3>";
      test.innerHTML+="<input type='radio' name='choicess' value='A'> "+a+"<br>";
      test.innerHTML+="<input type='radio' name='choicess' value='B'> "+b+"<br>";
      test.innerHTML+="<input type='radio' name='choicess' value='C'> "+c+"<br>";
      test.innerHTML+="<input type='radio' name='choicess' value='D'> "+d+"<br>";
      test.innerHTML+="<button onclick='checkanswer()'>Submit Answer</button>";
    }
    function checkanswer(){
        var choices;
        choices=document.getElementsByTagName("input");
        for (var i=0;i<choices.length;i++){
          if(choices[i].checked){
            choice=choices[i].value;
          }
        }
        if(choice=='A'){
          correct=correct+5;
          console.log(correct);
        }
    }
    pos++;
    renderQuestion();
  }
