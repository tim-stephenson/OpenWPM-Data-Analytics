import {parse} from "acorn";

const code : string = (`
console.log(parse("1 + 1", {
     ecmaVersion: 2022,
    sourceType: "script"
     }
     ));
`);

console.log(parse(code, {
     ecmaVersion: 2022,
    sourceType: "script"
     }
     ));