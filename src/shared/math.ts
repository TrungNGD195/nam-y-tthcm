import katex from 'katex';
import 'katex/dist/katex.min.css';

export function renderMath(root: ParentNode): void {
  root.querySelectorAll<HTMLElement>('[data-math]').forEach(element => {
    katex.render(element.dataset.math ?? '', element, { throwOnError: false, trust: false, displayMode: element.dataset.mathDisplay !== 'false', output: 'htmlAndMathml' });
    element.removeAttribute('data-math');
  });
}
