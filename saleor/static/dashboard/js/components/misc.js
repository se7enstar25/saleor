import SVGInjector from 'svg-injector-2';

import { initSelects } from './utils';

export default $(document).ready((e) => {
  new SVGInjector().inject(document.querySelectorAll('svg[data-src]'));

  initSelects();
  $('.modal').modal();

  // Print button
  $('.btn-print').click((e) => {
    window.print();
  });

  // Clickable rows in dashboard tables
  $(document).on('click', 'tr[data-action-go]>td:not(.ignore-link)', function () {
    let target = $(this).parent();
    window.location.href = target.data('action-go');
  });

  $('#product-is-published').on('click', (e) => {
    const input = $(e.currentTarget).find('input')[0];
    if (e.target === input) {
      const url = $(e.currentTarget).attr('data-url');
      fetch(url, {
        credentials: 'same-origin'
      }).then((r) => {
        return r.json();
      }).then((r) => {
        const label = r.is_published ?
          pgettext('Product field', 'Published') :
          pgettext('Product field', 'Draft');
        $(e.currentTarget).find('.label').text(label);
      });
    }
    return 1;
  });
});
