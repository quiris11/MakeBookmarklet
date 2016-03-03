import sublime, sublime_plugin, re, urllib

EXISTING_JS_COMMENT_RE          = re.compile(r'^// ?javascript:.+', re.M)

KILL_COMMENTS_RE                = re.compile('^\s*//.+\n', re.M)
TABS_TO_SPACES_RE               = re.compile('\t', re.M)
SPACE_RUNS_TO_ONE_SPACE_RE      = re.compile('[ ]{2,}', re.M)
KILL_LINE_LEADING_WHITESPACE_RE = re.compile('^\s+', re.M)
KILL_LINE_ENDING_WHITESPACE_RE  = re.compile('\s+$', re.M)
KILL_NEWLINES_RE                = re.compile('\n', re.M)

class MakeBookmarkletCommand(sublime_plugin.TextCommand):
	'''
	Converts a JavaScript file into a 'javascript:' URL that can be safely
	used as a bookmarklet.

	This is just a Python/Sublime Text version of the Perl verion from
	http://daringfireball.net/2007/03/javascript_bookmarklet_builder
	'''
	def run(self, edit):
		v = self.view
		
		# Zap the first line if there's already a bookmarklet comment:
		first_line = v.full_line(0)
		if (EXISTING_JS_COMMENT_RE.match(v.substr(first_line))):
			v.replace(edit, first_line, '')

		text_region = sublime.Region(0, v.size())
		bookmarklet = v.substr(sublime.Region(0, v.size()))

		bookmarklet = KILL_COMMENTS_RE.sub('', bookmarklet)
		bookmarklet = TABS_TO_SPACES_RE.sub(' ', bookmarklet)
		bookmarklet = SPACE_RUNS_TO_ONE_SPACE_RE.sub(' ', bookmarklet)
		bookmarklet = KILL_LINE_LEADING_WHITESPACE_RE.sub('', bookmarklet)
		bookmarklet = KILL_LINE_ENDING_WHITESPACE_RE.sub('', bookmarklet)
		bookmarklet = KILL_NEWLINES_RE.sub('', bookmarklet)

		# Quotes all special characters. This is probably more aggressive than
		# needed, but the result isn't reable anyway and this is simple.
		bookmarklet = 'javascript:' + urllib.parse.quote(bookmarklet, '/()[]{}-_=;!?') + '\n'
		v.insert(edit, 0, '// ' + bookmarklet)

		# The real time saver is to just shove this on the clipboard directly.
		# A bit rude, but that's what clipboard history is for.
		sublime.set_clipboard(bookmarklet)
