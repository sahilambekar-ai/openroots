const fs=require('fs'),path=require('path'),ts=require(process.cwd()+'/node_modules/typescript');
const config=ts.readConfigFile('tsconfig.json',ts.sys.readFile).config;const parsed=ts.parseJsonConfigFileContent(config,ts.sys,process.cwd());const program=ts.createProgram(parsed.fileNames,parsed.options),checker=program.getTypeChecker();
const root='/Users/sahil/Documents/work/openroots/audit-evidence/2026-10-27/functional-review';const routes=JSON.parse(fs.readFileSync(root+'/routes.json','utf8'));const rows=[];
const combine=(a,b)=>a.flatMap(x=>b.map(y=>x+y)).slice(0,32);
function values(n,seen=new Set()){
 if(!n)return ['{dynamic}'];if(ts.isParenthesizedExpression(n))return values(n.expression,seen);
 if(ts.isStringLiteral(n)||ts.isNoSubstitutionTemplateLiteral(n))return [n.text];
 if(ts.isTemplateExpression(n)){let out=[n.head.text];for(const s of n.templateSpans)out=combine(out,values(s.expression,new Set(seen))).map(x=>x+s.literal.text);return out;}
 if(ts.isConditionalExpression(n))return [...values(n.whenTrue,new Set(seen)),...values(n.whenFalse,new Set(seen))];
 if(ts.isBinaryExpression(n)&&n.operatorToken.kind===ts.SyntaxKind.PlusToken)return combine(values(n.left,new Set(seen)),values(n.right,new Set(seen)));
 if(ts.isBinaryExpression(n)&&[ts.SyntaxKind.BarBarToken,ts.SyntaxKind.QuestionQuestionToken].includes(n.operatorToken.kind))return [...values(n.left,new Set(seen)),...values(n.right,new Set(seen))];
 if(ts.isIdentifier(n)){const symbol=checker.getSymbolAtLocation(n);if(symbol&&!seen.has(symbol)){seen.add(symbol);const d=symbol.valueDeclaration;if(d&&ts.isVariableDeclaration(d)&&d.initializer)return values(d.initializer,seen);}return ['{'+n.text+'}'];}
 return ['{dynamic}'];
}
function canonical(s){s=s.replace(/^https?:\/\/[^/]+/,'').replace(/^\{[^}]+\}(?=\/)/,'').split('?')[0];return s.replace(/\{[^}]+\}/g,'{}').replace(/\/$/,'')||'/';}
for(const source of program.getSourceFiles()){if(!source.fileName.includes('/src/')||source.isDeclarationFile)continue;function visit(n){if(ts.isCallExpression(n)&&/^(fetch|staffApi|get|post|request|api|apiFetch|communicationFetch)$/.test(n.expression.getText(source))){const name=n.expression.getText(source);let methods=[name==='post'?'POST':'GET'];const o=n.arguments[1];if(o&&ts.isObjectLiteralExpression(o)){const m=o.properties.find(p=>ts.isPropertyAssignment(p)&&p.name.getText(source)==='method');if(m)methods=values(m.initializer).map(x=>x.toUpperCase());}
 const patterns=[...new Set(values(n.arguments[0]).map(canonical))];const matches=routes.filter(r=>methods.some(m=>r.methods.includes(m))&&patterns.some(p=>p===r.path.replace(/\{[^}]+\}/g,'{}')));rows.push({file:path.relative(process.cwd(),source.fileName),line:source.getLineAndCharacterOfPosition(n.getStart()).line+1,helper:name,methods,patterns,matches:matches.map(r=>r.methods.join(',')+' '+r.path)});}
 ts.forEachChild(n,visit);}visit(source);}
fs.writeFileSync(root+'/client-route-matches.json',JSON.stringify(rows,null,2));console.log('Calls',rows.length,'matched',rows.filter(r=>r.matches.length).length);for(const row of rows.filter(r=>!r.matches.length))console.log(row.file+':'+row.line,JSON.stringify(row.methods),JSON.stringify(row.patterns));
