import{o as w,x as h,r as o,g,a as b,c as y,d as e,v as _,z as i,B as u,b as V,w as q,u as k,n as x,R}from"./index-4086a49a.js";import{c as B}from"./index-e096127b.js";const S={id:"signup"},U=e("section",{class:"md"},[e("h2",null,"Registrar")],-1),C=e("small",null,[e("em",null," verifica se digitou corretamente todos os campos. ")],-1),N=[C],z=e("small",null,[e("em",null," as palavras passe são diferente. ")],-1),D=[z],E={class:"md"},M=e("label",{for:"username"},"Name",-1),P={class:"md"},J=e("label",{for:"email"},"E-mail",-1),L={class:"md"},T=e("label",{for:"password1"},"Palavra passe",-1),j={class:"md"},A=e("label",{for:"password2"},"Confirma a Palavra passe",-1),F=e("small",null,"Ja tenho uma conta",-1),G=e("section",null,[e("button",null,"Registrar")],-1),O={__name:"SignupView",setup(H){w(()=>B.update_title("Signup"));const v=h(),l=o(""),n=o(""),t=o(""),r=o(""),d=o(!1),p=o(!1),c=g(),f=async m=>{if(m.preventDefault(),t.value.trim()!==r.value.trim()){p.value=!0;return}c.set(!0);const s=await x.post("/api/v1/users/",{name:l.value,email:n.value,password:t.value,is_admin:!1},!1,()=>c.set(!1));s.id?(l.value="",n.value="",t.value="",r.value="",v.replace("/auth/login")):(d.value=!0,console.log(s))};return(m,s)=>(b(),y("div",S,[e("form",{onSubmit:f},[U,e("section",{class:_(["error",d.value?"block-display":"none-display"])},N,2),e("section",{class:_(["error",p.value?"block-display":"none-display"])},D,2),e("section",E,[M,i(e("input",{"onUpdate:modelValue":s[0]||(s[0]=a=>l.value=a),type:"name",id:"name",required:""},null,512),[[u,l.value]])]),e("section",P,[J,i(e("input",{"onUpdate:modelValue":s[1]||(s[1]=a=>n.value=a),type:"email",id:"email",required:""},null,512),[[u,n.value]])]),e("section",L,[T,i(e("input",{"onUpdate:modelValue":s[2]||(s[2]=a=>t.value=a),type:"password",id:"password1",required:"",autocomplete:"new-password"},null,512),[[u,t.value]])]),e("section",j,[A,i(e("input",{"onUpdate:modelValue":s[3]||(s[3]=a=>r.value=a),type:"password",id:"password2",required:"",autocomplete:"new-password"},null,512),[[u,r.value]]),e("div",null,[V(k(R),{to:"/auth/login"},{default:q(()=>[F]),_:1})])]),G],32)]))}};export{O as default};
